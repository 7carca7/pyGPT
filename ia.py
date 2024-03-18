"OpenAI and Database classes"

import shelve
from tkinter.filedialog import asksaveasfilename
import os
import requests
from openai import OpenAI, AuthenticationError, OpenAIError


class Database:
    "Database Structure"

    def __init__(self):
        self.conn = None

    def open(self):
        "Open the DB"
        if not os.path.exists("database"):
            os.makedirs("database")
        self.conn = shelve.open("database/iaDB")

    def get_data(self):
        "Gets and returns the values stored in the DB"
        self.open()
        if self.conn is not None:
            key = self.conn.get("key")
            modelo = self.conn.get("modelo")
            if "contexto" not in self.conn:
                self.conn["contexto"] = [
                    {"role": "system", "content": "You are a useful virtual assistant"}]
            contexto = self.conn.get("contexto")
            url = self.conn.get("url")
            self.close()
            return key, modelo, contexto, url

        return None, None, None, None

    def enter_data(self, lugar, data):
        "Add information to the DB with the Place-Data scheme"
        self.open()
        if self.conn is not None:
            self.conn[lugar] = data
            self.close()

    def close(self):
        "Close the DB"
        if self.conn is not None:
            self.conn.close()


class Openai:
    "AI structure"

    def __init__(self):
        self.database = Database()
        api_key = self.database.get_data()[0]
        if api_key is not None:
            self.client = OpenAI(api_key=str(api_key))
        else:
            self.client = OpenAI(api_key="")
        self.db_modelo = self.database.get_data()[1]
        self.db_contexto = self.database.get_data()[2]
        self.url = self.database.get_data()[3]

    def ask(self, user_entry):
        "From the user's question returns an answer and adds it to a context"
        self.update()
        if self.db_contexto is not None:
            self.db_contexto.append({"role": "user", "content": user_entry})
            try:
                respuesta = self.client.chat.completions.create(
                    model=str(self.db_modelo), messages=self.db_contexto)
                respuesta = respuesta.choices[0].message.content
                self.db_contexto.append(
                    {"role": "assistant", "content": respuesta})
                return respuesta

            except AuthenticationError:
                # Capture the authentication error and display an appropriate message to the user
                return "Invalid API Key"

            except OpenAIError:
                # Capture other OpenAI errors and display an appropriate message to the user
                return "Model not found"
        return None

    def update(self):
        "Synchronize and compare the values of the DB with those of the application instance"
        if self.client.api_key != self.database.get_data()[0]:
            self.client.api_key = str(self.database.get_data()[0])
        if self.db_modelo != self.database.get_data()[1]:
            self.db_modelo = self.database.get_data()[1]

    def create_image(self, user_entry):
        "Create an image from a user description"
        response = self.client.images.generate(
            model="dall-e-3", prompt=user_entry, size="1024x1024", quality="standard", n=1)
        imagen_url = response.data[0].url
        self.database.enter_data("url", imagen_url)
        return imagen_url

    def save(self):
        "Save the generated image in the system"
        url = self.database.get_data()[3]
        if url is None:
            raise ValueError("URL is None")
        response = requests.get(url, timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)

    def restart(self):
        "Restarts the DB context"
        self.db_contexto = self.database.get_data()[2]

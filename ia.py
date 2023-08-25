"OpenAI and Database classes"

import shelve
from tkinter.filedialog import asksaveasfilename
import os
import openai
import requests


class Database:
    "Database Structure"

    def __init__(self):
        self.conn = None

    def open(self):
        "Open the DB"
        if not os.path.exists("database"):
            os.makedirs("database")
        self.conn = shelve.open("database/iaDB")

    def obtener_data(self):
        "Gets and returns the values stored in the DB"
        self.open()
        key = self.conn.get("key")
        modelo = self.conn.get("modelo")
        if "contexto" not in self.conn:
            self.conn["contexto"] = [
                {"role": "system", "content": "You are a useful virtual assistant"}]
        contexto = self.conn.get("contexto")
        url = self.conn.get("url")
        self.close()
        return key, modelo, contexto, url

    def ingresar_data(self, lugar, data):
        "Add information to the DB with the Place-Data scheme"
        self.open()
        self.conn[lugar] = data
        self.close()

    def close(self):
        "Close the DB"
        self.conn.close()


class OpenAI:
    "AI structure"

    def __init__(self):
        self.database = Database()
        openai.api_key, self.db_modelo, self.db_contexto, self.url = self.database.obtener_data()

    def preguntar(self, user_entry):
        "From the user's question returns an answer and adds it to a context"
        self.actualizar()
        self.db_contexto.append({"role": "user", "content": user_entry})
        respuesta = openai.ChatCompletion.create(
            model=self.db_modelo, messages=self.db_contexto)
        respuesta = respuesta.choices[0].message.content
        self.db_contexto.append({"role": "assistant", "content": respuesta})
        return respuesta

    def actualizar(self):
        "Synchronize and compare the values of the DB with those of the application instance"
        if openai.api_key != self.database.obtener_data()[0]:
            openai.api_key = self.database.obtener_data()[0]
        if self.db_modelo != self.database.obtener_data()[1]:
            self.db_modelo = self.database.obtener_data()[1]

    def crear_imagen(self, user_entry):
        "Create an image from a user description"
        response = openai.Image.create(
            prompt=user_entry, n=1, size="1024x1024")
        imagen_url = response['data'][0]['url']
        self.database.ingresar_data("url", imagen_url)
        return imagen_url

    def guardar(self):
        "Save the generated image in the system"
        response = requests.get(self.database.obtener_data()[3], timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)

    def reiniciar(self):
        "Restarts the DB context"
        self.db_contexto = self.database.obtener_data()[2]

import shelve
import openai
import requests
from tkinter.filedialog import asksaveasfilename


# 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


class Database:
    def __init__(self):
        self.conn = shelve.open("iaDB")

    def obtener_data(self):
        key = self.conn.get("key")
        modelo = self.conn.get("modelo")
        contexto = self.conn.get("contexto")

        return key, modelo, contexto

    def ingresar_data(self, lugar, dato):
        self.conn[lugar] = dato

    def close(self):
        self.conn.close()


# db = Database()
# db.ingresar_data(
#    lugar="key", dato="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")
# db.ingresar_data(lugar="modelo", dato="gpt-3.5-turbo")
# db.ingresar_data(lugar="contexto", dato=[
#                 {"role": "system", "content": "Eres un asistente virtual útil"}])


class OpenAI:
    def __init__(self):
        db = Database()
        self.openai_key, self.db_modelo, self.db_contexto = db.obtener_data()
        openai.api_key = self.openai_key

    def preguntar(self, user_entry):
        "Devuelve la respuesta de chatGPT"
        self.db_contexto.append(
            {"role": "user", "content": user_entry})
        respuesta = openai.ChatCompletion.create(
            model=self.db_modelo, messages=self.db_contexto)
        respuesta = respuesta.choices[0].message.content
        self.db_contexto.append(
            {"role": "assistant", "content": respuesta})
        return print(respuesta)

    def crear_imagen(self, user_entry):
        "Toma una descripción y crea una imagen con ella"
        response = openai.Image.create(
            prompt=user_entry, n=1, size="1024x1024")
        imagen_url = response['data'][0]['url']
        return print(imagen_url)

    def guardar(self):
        "Guarda la imagen en el almacenamiento del sistema"
        response = requests.get(self.crear_imagen(), timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)

    def reiniciar(self):
        "Reinicia la lista que almacena el contexto de la coversación"
        self.db_contexto = [
            {"role": "system", "content": "Eres un asistente virtual útil"}]


# ia = OpenAI()
# ia.crear_imagen(user_entry="un atardecer en la habana")
# while True:
#    ia.preguntar(user_entry=input())

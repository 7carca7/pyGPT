"Clases OpenAI y Database"

import shelve
from tkinter.filedialog import asksaveasfilename
import openai
import requests


class Database:
    "Estructura de la clase Database"

    def __init__(self):
        self.conn = None

    def open(self):
        "Abre la database"
        self.conn = shelve.open("iaDB")

    def obtener_data(self):
        "Obtiene y devuelve los valores alojados en la DB"
        self.open()
        key = self.conn.get("key")
        modelo = self.conn.get("modelo")
        if "contexto" not in self.conn:
            self.conn["contexto"] = [
                {"role": "system", "content": "Eres un asistente virtual útil"}]
        contexto = self.conn.get("contexto")
        url = self.conn.get("url")
        self.close()
        return key, modelo, contexto, url

    def ingresar_data(self, lugar, data):
        "Ingresa información a la DB con el esquema Lugar-Data"
        self.open()
        self.conn[lugar] = data
        self.close()

    def close(self):
        "Cierra la DB"
        self.conn.close()


class OpenAI:
    "Estructura de la IA"

    def __init__(self):
        self.database = Database()
        openai.api_key, self.db_modelo, self.db_contexto, self.url = self.database.obtener_data()

    def preguntar(self, user_entry):
        "A partir de la pregunta del usuario devuelve una respuesta y la agrega a un contexto"
        self.actualizar()
        self.db_contexto.append({"role": "user", "content": user_entry})
        respuesta = openai.ChatCompletion.create(
            model=self.db_modelo, messages=self.db_contexto)
        respuesta = respuesta.choices[0].message.content
        self.db_contexto.append({"role": "assistant", "content": respuesta})
        return respuesta

    def actualizar(self):
        "Sincroniza y compara los valores de la DB com los de la instancia de la aplicación"
        if openai.api_key != self.database.obtener_data()[0]:
            openai.api_key = self.database.obtener_data()[0]
        if self.db_modelo != self.database.obtener_data()[1]:
            self.db_modelo = self.database.obtener_data()[1]

    def crear_imagen(self, user_entry):
        "Crea una imagen a partir de una descripción del usuario"
        response = openai.Image.create(
            prompt=user_entry, n=1, size="1024x1024")
        imagen_url = response['data'][0]['url']
        self.database.ingresar_data("url", imagen_url)
        return imagen_url

    def guardar(self):
        "Guarda la imagen generada en el sistema"
        response = requests.get(self.database.obtener_data()[3], timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)

    def reiniciar(self):
        "Reinicia el contexto de la DB"
        self.db_contexto = self.database.obtener_data()[2]

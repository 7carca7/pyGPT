import shelve
import openai
import requests
from tkinter.filedialog import asksaveasfilename


class Database:
    def __init__(self):
        self.conn = shelve.open("iaDB")

    def obtener_data(self):
        key = self.conn.get("key")
        modelo = self.conn.get("modelo")
        contexto = self.conn.get("contexto")

        return key, modelo, contexto

    def ingresar_data(self, lugar, data):
        self.conn[lugar] = data

    def close(self):
        self.conn.close()


class OpenAI:
    def __init__(self):
        self.db = Database()
        self.openai_key, self.db_modelo, self.db_contexto = self.db.obtener_data()
        openai.api_key = self.openai_key
        if self.db_contexto is None:
            self.db_contexto = [
                {"role": "system", "content": "Eres un asistente virtual útil"}]

    def preguntar(self, user_entry):
        self.db_contexto.append({"role": "user", "content": user_entry})
        respuesta = openai.ChatCompletion.create(
            model=self.db_modelo, messages=self.db_contexto)
        respuesta = respuesta.choices[0].message.content
        self.db_contexto.append({"role": "assistant", "content": respuesta})
        return respuesta

    def crear_imagen(self, user_entry):
        response = openai.Image.create(
            prompt=user_entry, n=1, size="1024x1024")
        imagen_url = response['data'][0]['url']
        return imagen_url

    def guardar(self):
        imagen_url = self.crear_imagen()
        response = requests.get(imagen_url, timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)

    def reiniciar(self):
        self.db_contexto = [
            {"role": "system", "content": "Eres un asistente virtual útil"}]


""" db = Database()
db.ingresar_data(
    lugar="key", data="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")
db.ingresar_data(lugar="modelo", data="gpt-3.5-turbo")
db.ingresar_data(lugar="contexto",data=[{"role": "system", "content": "Eres muy gracioso"}])
db.close() """

ia = OpenAI()
print(ia.openai_key)
print(ia.db_modelo)
print(ia.db_contexto)

while True:
    user_input = input("User: ")
    response = ia.preguntar(user_input)
    print("Assistant:", response)

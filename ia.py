import shelve
import openai
import requests
from tkinter.filedialog import asksaveasfilename


class Database:
    def __init__(self):
        self.conn = shelve.open("iaDB")

    def obtener_data(self):
        self.__init__()
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
        self.__init__()
        self.conn[lugar] = data
        self.close()

    def close(self):
        self.conn.close()


class OpenAI:
    def __init__(self):
        self.db = Database()
        self.db.__init__()
        self.openai_key, self.db_modelo, self.db_contexto, self.url = self.db.obtener_data()
        openai.api_key = self.openai_key
        # if self.db_contexto == "" or self.db_contexto is None:
        #    self.db_contexto = [
        #        {"role": "system", "content": "Eres un asistente virtual útil"}]

        self.db.close()

    def preguntar(self, user_entry):
        self.db_contexto.append({"role": "user", "content": user_entry})
        respuesta = openai.ChatCompletion.create(
            model=self.db_modelo, messages=self.db_contexto)
        respuesta = respuesta.choices[0].message.content
        self.db_contexto.append({"role": "assistant", "content": respuesta})
        # print(self.db_contexto)
        # self.db.__init__()
        # print(self.db.obtener_data()[2])
        # self.db.close()
        print(respuesta)

        return respuesta

    def crear_imagen(self, user_entry):
        self.db.__init__()
        response = openai.Image.create(
            prompt=user_entry, n=1, size="1024x1024")
        imagen_url = response['data'][0]['url']
        self.db.ingresar_data("url", imagen_url)
        self.db.close()
        return imagen_url

    def guardar(self):
        # imagen_url = self.url
        self.db.__init__()
        response = requests.get(self.db.obtener_data()[3], timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)
        self.db.close()

# por hacer:
# aqui el contexto debe ser el que le ingreso el usuario a la BD y si no hay ninguno tomar este
    def reiniciar(self):
        self.db_contexto = [
            {"role": "system", "content": "Eres un asistente virtual útil"}]


""" db = Database()
db.ingresar_data(
    lugar="key", data="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")
db.ingresar_data(lugar="modelo", data="gpt-3.5-turbo")
db.ingresar_data(lugar="contexto",data=[{"role": "system", "content": "Eres muy gracioso"}])
db.close() """

""" ia = OpenAI()
print(ia.openai_key)
print(ia.db_modelo)
print(ia.db_contexto)

while True:
    user_input = input("User: ")
    response = ia.preguntar(user_input)
    print("Assistant:", response) """

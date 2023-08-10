import shelve
import openai
import requests
from tkinter.filedialog import asksaveasfilename


class Database:
    def __init__(self):
        self.conn = shelve.open("iaDB")

    def obtener_data(self):
        "Obtiene y devuelve los valores alojados en la DB"
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
        "Ingresa información a la DB con el esquema Lugar-Data"
        self.__init__()
        self.conn[lugar] = data
        self.close()

    def close(self):
        "Cierra la DB"
        self.conn.close()


class OpenAI:
    def __init__(self):
        self.db = Database()
        self.db.__init__()
        self.openai_key, self.db_modelo, self.db_contexto, self.url = self.db.obtener_data()
        openai.api_key = self.openai_key
        self.db.close()

    def preguntar(self, user_entry):
        "A partir de la pregunta del usuario devuelve una respuesta y la agrega a un contexto"
        self.db_contexto.append({"role": "user", "content": user_entry})
        respuesta = openai.ChatCompletion.create(
            model=self.db_modelo, messages=self.db_contexto)
        respuesta = respuesta.choices[0].message.content
        self.db_contexto.append({"role": "assistant", "content": respuesta})
        return respuesta

    def crear_imagen(self, user_entry):
        "Crea una imagen a partir de una descripción del usuario"
        self.db.__init__()
        response = openai.Image.create(
            prompt=user_entry, n=1, size="1024x1024")
        imagen_url = response['data'][0]['url']
        self.db.ingresar_data("url", imagen_url)
        self.db.close()
        return imagen_url

    def guardar(self):
        "Guarda la imagen generada en el sistema"
        self.db.__init__()
        response = requests.get(self.db.obtener_data()[3], timeout=10)
        ruta_guardado = asksaveasfilename(defaultextension=".png")
        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)
        self.db.close()

    def reiniciar(self):
        "Reinicia el contexto de la DB"
        self.db_contexto = self.db.obtener_data()[2]

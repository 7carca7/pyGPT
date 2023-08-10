from ia import Database, OpenAI

import webbrowser
import customtkinter as ctk


class Config:
    def __init__(self):
        self.db = Database()
        # self.ia = OpenAI()

    # def aplicar(self, lugar, data):
    #    "Aplica los cambios de configuración"
    #
    #    self.db.ingresar_data(lugar, data)

    def aplicar(self, valor_key, valor_modelo, valor_contexto):
        self.db.__init__()
        self.key = valor_key
        self.modelo = valor_modelo
        self.contexto = valor_contexto

        if self.key != "":
            self.db.ingresar_data("key", valor_key)
            print(self.key, type(self.key))

        if self.modelo != "":
            self.db.ingresar_data("modelo", self.modelo)
            print(self.modelo, type(self.modelo))

        if self.contexto != "":
            self.db.ingresar_data(
                "contexto", [{"role": "system", "content": self.contexto}])
            print(self.contexto, type(self.contexto))

        self.db.close()
        #OpenAI.reinicializar(self)

    def abrir_enlace(self, url):
        "Abre los enlaces de ayuda"

        webbrowser.open_new(url)

    def change_scaling_event(self, new_scaling: str):
        "Cambia la escala de la UI"

        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

        # key = entrada_key.get()
        # modelo = entrada_modelo.get()
        # contexto = entrada_contexto.get()

        # if key and modelo and contexto:
        #    conf.aplicar(key, modelo, contexto)

from ia import Database

import webbrowser
import customtkinter as ctk


class Config:
    def __init__(self):
        self.db = Database()

    # def aplicar(self, lugar, data):
    #    "Aplica los cambios de configuración"
    #
    #    self.db.ingresar_data(lugar, data)

    def aplicar(self, valor_key, valor_modelo, valor_contexto):
        self.key = valor_key
        self.modelo = valor_modelo
        self.contexto = valor_contexto

        if self.key != "" or self.key is None:
            self.db.ingresar_data("key", self.key)
        if self.modelo != "" or self.modelo is None:
            self.db.ingresar_data("modelo", self.modelo)
        if self.contexto != "" or self.contexto is None:
            self.db.ingresar_data("contexto", self.contexto)

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

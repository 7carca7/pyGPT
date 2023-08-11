from ia import Database

import webbrowser
import customtkinter as ctk


class Config:
    def __init__(self):
        self.db = Database()

    def aplicar(self, valor_key, valor_modelo, valor_contexto):
        "Si hay datos nuevos en los campos de Settings los ingresa en la DB"
        self.db.__init__()
        self.key = valor_key
        self.modelo = valor_modelo
        self.contexto = valor_contexto

        if self.key != "":
            self.db.ingresar_data("key", self.key)
        if self.modelo != "":
            self.db.ingresar_data("modelo", self.modelo)
        if self.contexto != "":
            self.db.ingresar_data(
                "contexto", [{"role": "system", "content": self.contexto}])
        self.db.close()

    def abrir_enlace(self, url):
        "Abre los enlaces de ayuda"
        webbrowser.open_new(url)

    def change_scaling_event(self, new_scaling: str):
        "Cambia la escala de la UI"
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

"Class for configuration"

import webbrowser
import customtkinter as ctk
from ia import Database


class Config:
    "Sets the configuration structure"

    def __init__(self):
        self.database = Database()

    def aplicar(self, valor_key, valor_modelo, valor_contexto):
        "If there is new data in the Settings fields, it enters it in the DB"
        if valor_key != "":
            self.database.ingresar_data("key", valor_key)
        if valor_modelo != "":
            self.database.ingresar_data("modelo", valor_modelo)
        if valor_contexto != "":
            self.database.ingresar_data(
                "contexto", [{"role": "system", "content": valor_contexto}])

    def abrir_enlace(self, url):
        "Open help links"
        webbrowser.open_new(url)

    def change_scaling_event(self, new_scaling: str):
        "Change the scale of the UI"
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

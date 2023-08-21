"Clase para la configuración"

import webbrowser
import customtkinter as ctk
from ia import Database


class Config:
    "Se establece la estructura de la configuración"

    def __init__(self):
        self.database = Database()

    def aplicar(self, valor_key, valor_modelo, valor_contexto):
        "Si hay datos nuevos en los campos de Settings los ingresa en la DB"
        if valor_key != "":
            self.database.ingresar_data("key", valor_key)
        if valor_modelo != "":
            self.database.ingresar_data("modelo", valor_modelo)
        if valor_contexto != "":
            self.database.ingresar_data(
                "contexto", [{"role": "system", "content": valor_contexto}])

    def abrir_enlace(self, url):
        "Abre los enlaces de ayuda"
        webbrowser.open_new(url)

    def change_scaling_event(self, new_scaling: str):
        "Cambia la escala de la UI"
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

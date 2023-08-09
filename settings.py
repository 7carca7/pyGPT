from ia import Database

import webbrowser
import customtkinter as ctk


class Config:
    def __init__(self):
        self.db = Database()

    def aplicar(self,key,modelo,contexto):
        "Aplica los cambios de configuración"

        self.db.ingresar_data(key,modelo,contexto)

    def abrir_enlace(self, url):
        "Abre los enlaces de ayuda"

        webbrowser.open_new(url)

    def change_scaling_event(self, new_scaling: str):
        "Cambia la escala de la UI"

        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

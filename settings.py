from ia import Database
import main


class Config:
    def __init__(self):
        self.db = Database()

    def aplicar(self):
        "Aplica los cambios de configuración"

        self.db.ingresar_data(lugar="key", dato=main.entrada_key.get())
        self.db.ingresar_data(lugar="modelo", dato=main.entrada_modelo.get())
        self.db.ingresar_data(
            lugar="contexto", dato=main.entrada_contexto.get())

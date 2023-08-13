"pyGPT es una interfaz gráfica para interactuar con Openai"

import urllib.request
import io
from PIL import Image
import customtkinter as ctk
from ia import OpenAI, Database
from settings import Config
from tabs_views.chat_view import ChatView
from tabs_views.imagen_view import ImagenView
from tabs_views.ajustes_view import AjustesView

# gpt-3.5-turbo
# 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

db = Database()
ia = OpenAI()
conf = Config()

app = ctk.CTk()
app.geometry("500x500")
app.title("pyGPT")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.minsize(350, 500)
MyTabView = ctk.CTkTabview(app)
"Sistema de pestañas"
MyTabView.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
MyTabView.configure(fg_color="transparent", segmented_button_selected_color="#1E90FF",
                    segmented_button_selected_hover_color="#1A7AD9")

# TABS
ChatView(MyTabView, ctk, ia)
ImagenView(MyTabView, ctk, ia, urllib, Image, io)
AjustesView(MyTabView, ctk, db, conf)

if __name__ == "__main__":
    app.mainloop()

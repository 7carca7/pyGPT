"pyGPT es una interfaz gráfica para interactuar con Openai"
#restaurar el key binding

import urllib.request
import io
from tkinter.filedialog import asksaveasfilename
from PIL import Image
import customtkinter as ctk
from ia import OpenAI, Database
from settings import Config

db = Database()
ia = OpenAI()
conf = Config()

# gpt-3.5-turbo
# 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

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

# PÁGINA CHAT

MyTabView.add("CHAT")
MyTabView.tab("CHAT").grid_columnconfigure(0, weight=1)
MyTabView.tab("CHAT").grid_rowconfigure(0, weight=1)

frame_principal = ctk.CTkFrame(
    MyTabView.tab("CHAT"), border_width=-10, fg_color="transparent")
frame_principal.grid(row=0, column=0, padx=6, sticky="nsew")
frame_principal.grid_rowconfigure(0, weight=1)
frame_principal.grid_columnconfigure(0, weight=1)


cuadro_superior = ctk.CTkFrame(master=frame_principal, fg_color="transparent")
cuadro_superior.grid(padx=0, pady=(0, 12), sticky="nswe")
cuadro_superior.grid_rowconfigure(0, weight=1)
cuadro_superior.grid_columnconfigure(0, weight=1)


salida = ctk.CTkTextbox(
    cuadro_superior, fg_color="transparent", scrollbar_button_color="#A8A8A8",
    scrollbar_button_hover_color="#A8A8A8")
salida.grid(row=0, column=0, sticky="nswe")
salida.configure(wrap="word")
salida.configure(state="disabled")


cuadro_inferior = ctk.CTkFrame(master=frame_principal, fg_color="transparent")
cuadro_inferior.grid(padx=0, pady=(0, 7), sticky="swe")
cuadro_inferior.grid_rowconfigure(0, weight=1)
cuadro_inferior.grid_columnconfigure(0, weight=3)
cuadro_inferior.grid_columnconfigure(1, weight=0)

entrada = ctk.CTkEntry(cuadro_inferior, placeholder_text_color="#A8A8A8",
                       placeholder_text="Ingrese una pregunta...")
entrada.grid(row=0, column=0, padx=(0, 9), sticky="we")
# entrada.bind('<Return>', ia.preguntar(entrada.get))

contenedor_botones = ctk.CTkFrame(cuadro_inferior, fg_color="transparent")
contenedor_botones.grid(row=0, column=1, sticky="ew")

boton_enviar = ctk.CTkButton(
    contenedor_botones, text="Enviar", command=lambda: enviar())
boton_enviar.grid(row=0, column=0, sticky="ew")
boton_enviar.configure(width=60, fg_color="#1E90FF", hover_color="#1A7AD9")


def enviar():
    respuesta = ia.preguntar(entrada.get())
    salida.configure(state="normal")
    salida.delete(0.0, ctk.END)
    salida.insert("0.0", respuesta)
    salida.configure(state="disabled")
    entrada.delete("0", "end")


boton_reiniciar = ctk.CTkButton(
    contenedor_botones, text="\u267A", font=("", 16), command=lambda: reiniciar())
boton_reiniciar.grid(row=0, column=1, padx=(10, 0), sticky="ew")
boton_reiniciar.configure(width=35, fg_color="#F28A30", hover_color="#CE7529")


def reiniciar():
    ia.reiniciar()
    salida.configure(state='normal')
    salida.delete(0.0, ctk.END)
    salida.configure(state='disabled')
    entrada.delete("0", "end")
    entrada.insert(0, "Conversación reiniciada...")


# PÁGINA IMAGEN

MyTabView.add("IMAGEN")
MyTabView.tab("IMAGEN").grid_columnconfigure(0, weight=1)
MyTabView.tab("IMAGEN").grid_rowconfigure(0, weight=1)

frame_imagen = ctk.CTkFrame(
    MyTabView.tab("IMAGEN"), border_width=-10, fg_color="transparent")
frame_imagen.grid(row=0, column=0, padx=6, sticky="nsew")
frame_imagen.grid_rowconfigure(0, weight=1)
frame_imagen.grid_columnconfigure(0, weight=1)


frame_salida_imagen = ctk.CTkFrame(frame_imagen, fg_color="transparent")
frame_salida_imagen.grid(row=0, column=0, pady=(0, 12), sticky="nswe")
frame_salida_imagen.grid_rowconfigure(0, weight=1)
frame_salida_imagen.grid_columnconfigure(0, weight=1)

frame_entrada_imagen = ctk.CTkFrame(frame_imagen, fg_color="transparent")
frame_entrada_imagen.grid(padx=0, pady=(0, 7), sticky="swe")
frame_entrada_imagen.grid_rowconfigure(0, weight=1)
frame_entrada_imagen.grid_columnconfigure(0, weight=3)
frame_entrada_imagen.grid_columnconfigure(1, weight=0)

entrada_imagen = ctk.CTkEntry(
    frame_entrada_imagen, placeholder_text_color="#A8A8A8",
    placeholder_text="Ingrese una descripción...")
entrada_imagen.grid(row=0, column=0, padx=(0, 9), sticky="we")
# entrada_imagen.bind('<Return>', ia.crear_imagen)

contenedor_botones_imagen = ctk.CTkFrame(
    frame_entrada_imagen, fg_color="transparent")
contenedor_botones_imagen.grid(row=0, column=1, sticky="ew")

boton_entrada_imagen = ctk.CTkButton(
    contenedor_botones_imagen, text="Crear", command=lambda: crear())
boton_entrada_imagen.grid(row=0, column=0, sticky="ew")
boton_entrada_imagen.configure(
    width=60, fg_color="#1E90FF", hover_color="#1A7AD9")


def crear():
    imagen_url = ia.crear_imagen(entrada_imagen.get())
    with urllib.request.urlopen(imagen_url) as url_datos:
        raw_data = url_datos.read()
    imagen_crear = Image.open(io.BytesIO(raw_data))
    photo = ctk.CTkImage(imagen_crear, size=(470, 405))
    label_imagen = ctk.CTkLabel(frame_salida_imagen, image=photo, text="")
    label_imagen.grid(row=0, column=0, sticky="nswe")
    entrada_imagen.delete("0", "end")


boton_descargar_imagen = ctk.CTkButton(
    contenedor_botones_imagen, text="\u2B07", command=lambda: ia.guardar())
boton_descargar_imagen.grid(row=0, column=1, padx=(10, 0), sticky="ew")
boton_descargar_imagen.configure(
    width=35, fg_color="#009E54", hover_color="#008D47")


# PÁGINA AJUSTES

MyTabView.add("AJUSTES")
MyTabView.tab("AJUSTES").grid_columnconfigure(0, weight=1)
MyTabView.tab("AJUSTES").grid_rowconfigure(0, weight=1)

frame_ajustes = ctk.CTkFrame(MyTabView.tab(
    "AJUSTES"), border_width=-10, fg_color="transparent")
frame_ajustes.grid(row=0, column=0, padx=6, sticky="nsew")
frame_ajustes.grid_rowconfigure(2, weight=1)
frame_ajustes.grid_columnconfigure(0, weight=1)


gpt_modelo = ctk.CTkFrame(frame_ajustes)
gpt_modelo.grid(row=0, column=0, sticky="new")
gpt_modelo.grid_columnconfigure(0, weight=1)
ev_label = ctk.CTkLabel(
    gpt_modelo, text="GPT Versión", text_color="#A8A8A8", font=("", 17))
ev_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
entrada_modelo = ctk.CTkEntry(
    gpt_modelo, placeholder_text_color="#A8A8A8",
    placeholder_text=db.obtener_data()[1])
entrada_modelo.grid(row=1, column=0, padx=(5, 5), pady=(0, 5), sticky="nsew")
enlace_modelo = ctk.CTkLabel(
    gpt_modelo, text="\u24D8 Modelos disponibles", text_color="#1E90FF", cursor="pointinghand")
enlace_modelo.grid(row=0, column=0, padx=5, sticky="e")
enlace_modelo.bind(
    "<Button-1>", lambda e: conf.abrir_enlace("https://platform.openai.com/docs/models/"))
# entrada_modelo.bind('<Return>', conf.aplicar)

api = ctk.CTkFrame(frame_ajustes)
api.grid(row=1, column=0, pady=(7, 0), sticky="new")
api.grid_columnconfigure(0, weight=1)
ek_label = ctk.CTkLabel(
    api, text="GPT Key", text_color="#A8A8A8", font=("", 17))
ek_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
entrada_key = ctk.CTkEntry(
    api, placeholder_text_color="#A8A8A8", placeholder_text=db.obtener_data()[0])
entrada_key.grid(row=1, column=0, padx=(5, 5), pady=(0, 5), sticky="nsew")
enlace_api = ctk.CTkLabel(
    api, text="\u24D8 Obtener una API-KEY", text_color="#1E90FF", cursor="pointinghand")
enlace_api.grid(row=0, column=0, padx=5, sticky="e")
enlace_api.bind(
    "<Button-1>", lambda e: conf.abrir_enlace("https://platform.openai.com/account/api-keys"))
# entrada_key.bind('<Return>', conf.aplicar)

contexto = ctk.CTkFrame(frame_ajustes)
contexto.grid(row=2, column=0, pady=(7, 0), sticky="new")
contexto.grid_columnconfigure(0, weight=3)
contexto.grid_columnconfigure(1, weight=0)
ec_label = ctk.CTkLabel(
    contexto, text="GPT Contexto", text_color="#A8A8A8", font=("", 17))
ec_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")

entrada_contexto = ctk.CTkEntry(
    contexto, placeholder_text_color="#A8A8A8", placeholder_text=db.obtener_data()[2][0]["content"])  # PREGUNTAS_RESPUESTAS[0]["content"]
entrada_contexto.grid(
    row=1, column=0, padx=(5, 5), pady=(0, 5), sticky="nsew")
enlace_contexto = ctk.CTkLabel(
    contexto, text="\u24D8 Acerca de los contextos", text_color="#1E90FF", cursor="pointinghand")
enlace_contexto.grid(row=0, column=0, padx=5, sticky="e")
enlace_contexto.bind("<Button-1>", lambda e: conf.abrir_enlace(
    "https://platform.openai.com/docs/guides/chat/introduction"))
# entrada_contexto.bind('<Return>', conf.aplicar)

frame_ajustes_inf = ctk.CTkFrame(
    MyTabView.tab("AJUSTES"), fg_color="transparent")
frame_ajustes_inf.grid(padx=6, pady=(0, 7), sticky="swe")
frame_ajustes_inf.grid_rowconfigure(0, weight=1)
frame_ajustes_inf.grid_columnconfigure(0, weight=3)
frame_ajustes_inf.grid_columnconfigure(1, weight=0)

esc_label = ctk.CTkLabel(
    frame_ajustes_inf, text="UI Escala", anchor="w", text_color="#A8A8A8", font=("", 17))
esc_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
opcion_esc = ctk.CTkOptionMenu(frame_ajustes_inf, values=["100%", "125%", "150%"],
                               fg_color="#1E90FF", button_color="#1E90FF",
                               button_hover_color="#1A7AD9", width=145,
                               command=conf.change_scaling_event)
opcion_esc.grid(row=1, column=0, sticky="w")

boton_aplicar = ctk.CTkButton(
    frame_ajustes_inf, text="Aplicar", command=lambda: conf.aplicar(entrada_key.get(), entrada_modelo.get(), entrada_contexto.get()))
boton_aplicar.grid(row=1, column=1, sticky="ew")
boton_aplicar.configure(width=60, fg_color="#1E90FF", hover_color="#1A7AD9")

app.mainloop()

class ImagenView:
    def __init__(self, MyTabView, ctk, ia, urllib, Image, io):

        MyTabView.add("IMAGEN")
        MyTabView.tab("IMAGEN").grid_columnconfigure(0, weight=1)
        MyTabView.tab("IMAGEN").grid_rowconfigure(0, weight=1)

        frame_imagen = ctk.CTkFrame(
            MyTabView.tab("IMAGEN"), border_width=-10, fg_color="transparent")
        frame_imagen.grid(row=0, column=0, padx=6, sticky="nsew")
        frame_imagen.grid_rowconfigure(0, weight=1)
        frame_imagen.grid_columnconfigure(0, weight=1)

        frame_salida_imagen = ctk.CTkFrame(
            frame_imagen, fg_color="transparent")
        frame_salida_imagen.grid(row=0, column=0, pady=(0, 12), sticky="nswe")
        frame_salida_imagen.grid_rowconfigure(0, weight=1)
        frame_salida_imagen.grid_columnconfigure(0, weight=1)

        frame_entrada_imagen = ctk.CTkFrame(
            frame_imagen, fg_color="transparent")
        frame_entrada_imagen.grid(padx=0, pady=(0, 7), sticky="swe")
        frame_entrada_imagen.grid_rowconfigure(0, weight=1)
        frame_entrada_imagen.grid_columnconfigure(0, weight=3)
        frame_entrada_imagen.grid_columnconfigure(1, weight=0)

        entrada_imagen = ctk.CTkEntry(
            frame_entrada_imagen, placeholder_text_color="#A8A8A8",
            placeholder_text="Ingrese una descripción...")
        entrada_imagen.grid(row=0, column=0, padx=(0, 9), sticky="we")
        entrada_imagen.bind('<Return>', lambda event: crear())

        contenedor_botones_imagen = ctk.CTkFrame(
            frame_entrada_imagen, fg_color="transparent")
        contenedor_botones_imagen.grid(row=0, column=1, sticky="ew")

        boton_entrada_imagen = ctk.CTkButton(
            contenedor_botones_imagen, text="Crear", command=lambda: crear())
        boton_entrada_imagen.grid(row=0, column=0, sticky="ew")
        boton_entrada_imagen.configure(
            width=60, fg_color="#1E90FF", hover_color="#1A7AD9")

        boton_descargar_imagen = ctk.CTkButton(
            contenedor_botones_imagen, text="\u2B07", command=lambda: ia.guardar())
        boton_descargar_imagen.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        boton_descargar_imagen.configure(
            width=35, fg_color="#009E54", hover_color="#008D47")

        def crear():
            "Crea una imagen a partir del prompt del usuario"
            imagen_url = ia.crear_imagen(entrada_imagen.get())
            with urllib.request.urlopen(imagen_url) as url_datos:
                raw_data = url_datos.read()
            imagen_crear = Image.open(io.BytesIO(raw_data))
            photo = ctk.CTkImage(imagen_crear, size=(470, 405))
            label_imagen = ctk.CTkLabel(
                frame_salida_imagen, image=photo, text="")
            label_imagen.grid(row=0, column=0, sticky="nswe")
            entrada_imagen.delete("0", "end")
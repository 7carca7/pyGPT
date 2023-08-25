"Module that handles the structure of the Chat tab"


class ChatView:
    "The UI of the Chat tab is defined"

    def __init__(self, my_tab_view, ctk, ai_model):

        def enviar():
            "Sends the user's question to the AI"
            respuesta = ai_model.preguntar(entrada.get())
            salida.configure(state="normal")
            salida.delete(0.0, ctk.END)
            salida.insert("0.0", respuesta)
            salida.configure(state="disabled")
            entrada.delete("0", "end")

        def reiniciar():
            "Tells the AI to restart the conversation context"
            ai_model.reiniciar()
            salida.configure(state='normal')
            salida.delete(0.0, ctk.END)
            salida.configure(state='disabled')
            entrada.delete("0", "end")
            entrada.insert(0, "Conversation restarted...")

        my_tab_view.add("CHAT")
        my_tab_view.tab("CHAT").grid_columnconfigure(0, weight=1)
        my_tab_view.tab("CHAT").grid_rowconfigure(0, weight=1)

        frame_principal = ctk.CTkFrame(
            my_tab_view.tab("CHAT"), border_width=-10, fg_color="transparent")
        frame_principal.grid(row=0, column=0, padx=6, sticky="nsew")
        frame_principal.grid_rowconfigure(0, weight=1)
        frame_principal.grid_columnconfigure(0, weight=1)

        cuadro_superior = ctk.CTkFrame(
            master=frame_principal, fg_color="transparent")
        cuadro_superior.grid(padx=0, pady=(0, 12), sticky="nswe")
        cuadro_superior.grid_rowconfigure(0, weight=1)
        cuadro_superior.grid_columnconfigure(0, weight=1)

        salida = ctk.CTkTextbox(
            cuadro_superior, fg_color="transparent", scrollbar_button_color="#A8A8A8",
            scrollbar_button_hover_color="#A8A8A8")
        salida.grid(row=0, column=0, sticky="nswe")
        salida.configure(wrap="word")
        salida.configure(state="disabled")

        cuadro_inferior = ctk.CTkFrame(
            master=frame_principal, fg_color="transparent")
        cuadro_inferior.grid(padx=0, pady=(0, 7), sticky="swe")
        cuadro_inferior.grid_rowconfigure(0, weight=1)
        cuadro_inferior.grid_columnconfigure(0, weight=3)
        cuadro_inferior.grid_columnconfigure(1, weight=0)

        entrada = ctk.CTkEntry(cuadro_inferior, placeholder_text_color="#A8A8A8",
                               placeholder_text="Enter a question...")
        entrada.grid(row=0, column=0, padx=(0, 9), sticky="we")
        entrada.bind('<Return>', lambda event: enviar())

        contenedor_botones = ctk.CTkFrame(
            cuadro_inferior, fg_color="transparent")
        contenedor_botones.grid(row=0, column=1, sticky="ew")

        boton_enviar = ctk.CTkButton(
            contenedor_botones, text="Enviar", command=enviar)
        boton_enviar.grid(row=0, column=0, sticky="ew")
        boton_enviar.configure(
            width=60, fg_color="#1E90FF", hover_color="#1A7AD9")

        boton_reiniciar = ctk.CTkButton(
            contenedor_botones, text="\u267A", font=("", 16), command=reiniciar)
        boton_reiniciar.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        boton_reiniciar.configure(
            width=35, fg_color="#F28A30", hover_color="#CE7529")

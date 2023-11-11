"Module that manages the structure of the Settings tab"


class SettingsView:
    "The UI of the Settings tab is defined"

    def __init__(self, my_tab_view, ctk, database, conf):

        my_tab_view.add("SETTINGS")
        my_tab_view.tab("SETTINGS").grid_columnconfigure(0, weight=1)
        my_tab_view.tab("SETTINGS").grid_rowconfigure(0, weight=1)

        frame_ajustes = ctk.CTkFrame(my_tab_view.tab(
            "SETTINGS"), border_width=-10, fg_color="transparent")
        frame_ajustes.grid(row=0, column=0, padx=6, sticky="nsew")
        frame_ajustes.grid_rowconfigure(2, weight=1)
        frame_ajustes.grid_columnconfigure(0, weight=1)

        api = ctk.CTkFrame(frame_ajustes)
        api.grid(row=0, column=0, sticky="new")
        api.grid_columnconfigure(0, weight=1)
        ek_label = ctk.CTkLabel(
            api, text="API Key", text_color="#A8A8A8", font=("", 17))
        ek_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
        entrada_key = ctk.CTkEntry(
            api, placeholder_text_color="#A8A8A8", placeholder_text=database.obtener_data()[0])
        entrada_key.grid(row=1, column=0, padx=(
            5, 5), pady=(0, 5), sticky="nsew")
        enlace_api = ctk.CTkLabel(
            api, text="\u24D8 Get an API Key", text_color="#1E90FF", cursor="hand2")
        enlace_api.grid(row=0, column=0, padx=5, sticky="e")
        enlace_api.bind(
            "<Button-1>",
            lambda e: conf.abrir_enlace("https://platform.openai.com/account/api-keys"))
        entrada_key.bind('<Return>', lambda event: conf.aplicar(
            entrada_key.get(), entrada_modelo.get(), entrada_contexto.get()))

        gpt_modelo = ctk.CTkFrame(frame_ajustes)
        gpt_modelo.grid(row=1, column=0, pady=(7, 0), sticky="new")
        gpt_modelo.grid_columnconfigure(0, weight=1)
        ev_label = ctk.CTkLabel(
            gpt_modelo, text="GPT Model", text_color="#A8A8A8", font=("", 17))
        ev_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
        entrada_modelo = ctk.CTkEntry(
            gpt_modelo, placeholder_text_color="#A8A8A8",
            placeholder_text=database.obtener_data()[1])
        entrada_modelo.grid(row=1, column=0, padx=(5, 5),
                            pady=(0, 5), sticky="nsew")
        enlace_modelo = ctk.CTkLabel(
            gpt_modelo, text="\u24D8 Available models",
            text_color="#1E90FF", cursor="hand2")
        enlace_modelo.grid(row=0, column=0, padx=5, sticky="e")
        enlace_modelo.bind(
            "<Button-1>", lambda e: conf.abrir_enlace("https://platform.openai.com/docs/models/"))
        entrada_modelo.bind('<Return>', lambda event: conf.aplicar(
            entrada_key.get(), entrada_modelo.get(), entrada_contexto.get()))

        contexto = ctk.CTkFrame(frame_ajustes)
        contexto.grid(row=2, column=0, pady=(7, 0), sticky="new")
        contexto.grid_columnconfigure(0, weight=3)
        contexto.grid_columnconfigure(1, weight=0)
        ec_label = ctk.CTkLabel(
            contexto, text="GPT Context", text_color="#A8A8A8", font=("", 17))
        ec_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")

        entrada_contexto = ctk.CTkEntry(
            contexto, placeholder_text_color="#A8A8A8",
            placeholder_text=database.obtener_data()[2][0]["content"])
        entrada_contexto.grid(
            row=1, column=0, padx=(5, 5), pady=(0, 5), sticky="nsew")
        enlace_contexto = ctk.CTkLabel(
            contexto, text="\u24D8 About contexts",
            text_color="#1E90FF", cursor="hand2")
        enlace_contexto.grid(row=0, column=0, padx=5, sticky="e")
        enlace_contexto.bind("<Button-1>", lambda e: conf.abrir_enlace(
            "https://platform.openai.com/docs/guides/chat/introduction"))
        entrada_contexto.bind('<Return>', lambda event: conf.aplicar(
            entrada_key.get(), entrada_modelo.get(), entrada_contexto.get()))

        frame_ajustes_inf = ctk.CTkFrame(
            my_tab_view.tab("SETTINGS"), fg_color="transparent")
        frame_ajustes_inf.grid(padx=6, pady=(0, 7), sticky="swe")
        frame_ajustes_inf.grid_rowconfigure(0, weight=1)
        frame_ajustes_inf.grid_columnconfigure(0, weight=3)
        frame_ajustes_inf.grid_columnconfigure(1, weight=0)

        esc_label = ctk.CTkLabel(
            frame_ajustes_inf, text="UI Scale", anchor="w", text_color="#A8A8A8", font=("", 17))
        esc_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        opcion_esc = ctk.CTkOptionMenu(frame_ajustes_inf, values=["100%", "125%", "150%"],
                                       fg_color="#1E90FF", button_color="#1E90FF",
                                       button_hover_color="#1A7AD9", width=145,
                                       command=conf.change_scaling_event)
        opcion_esc.grid(row=1, column=0, sticky="w")

        boton_aplicar = ctk.CTkButton(
            frame_ajustes_inf, text="Apply", command=lambda:
            conf.aplicar(entrada_key.get(), entrada_modelo.get(), entrada_contexto.get()))
        boton_aplicar.grid(row=1, column=1, sticky="ew")
        boton_aplicar.configure(
            width=60, fg_color="#1E90FF", hover_color="#1A7AD9")

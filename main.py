"""pyGPT is a graphical interface to interact with the Openai API"""

from PIL import Image
import customtkinter as ctk
from ia import OpenAI, Database
from settings import Config
from tabs.chat_view import ChatView
from tabs.image_view import ImageView
from tabs.settings_view import SettingsView


db = Database()
ia = OpenAI()
conf = Config()

# MAIN APP
app = ctk.CTk()
app.geometry("500x500")
app.title("pyGPT")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.minsize(350, 500)
MyTabView = ctk.CTkTabview(app)

# TABS SYSTEM
MyTabView.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
MyTabView.configure(fg_color="transparent",
                    segmented_button_selected_color="#1E90FF",
                    segmented_button_selected_hover_color="#1A7AD9")

# TABS
ChatView(MyTabView, ctk, ia)
ImageView(MyTabView, ctk, ia, Image)
SettingsView(MyTabView, ctk, db, conf)

# RUN APP
if __name__ == "__main__":
    app.mainloop()

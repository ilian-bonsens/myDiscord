import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class Inscription:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_gui()

    def clear_entry(self, event, entry):
        entry.delete(0, tk.END)

    def open_inscription(self):
        # Importer le contenu de inscription.py
        import inscription

    def toggle_password_visibility(self, entry):
        if entry.cget('show') == '*':
            entry.configure(show='')
        else:
            entry.configure(show='*')

    def setup_gui(self):
        self.root.title("Discord IML")
        self.root.geometry("1280x720")
        self.root.configure(bg='black')

        # Charger l'image de fond
        image = Image.open("images/page2.png")
        image = image.resize((1280, 720), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image  # Gardez une référence de l'image

        custom_font = ("Gill Sans MT", 14)

        self.create_entry("Nom", 300)
        self.create_entry("Prénom", 360)
        self.create_entry("E-mail", 420)
        self.create_password_entry(480)

        self.add_buttons()

        self.root.mainloop()

    def create_entry(self, placeholder, y):
        entry = ctk.CTkEntry(self.root, width=250, font=("Gill Sans MT", 14), justify='center')
        entry.place(x=640, y=y, anchor='center')
        entry.configure(placeholder_text=placeholder, fg_color="black", text_color="#9489ae", placeholder_text_color="#9489ae", corner_radius=0)

    def create_password_entry(self, y):
        entry = ctk.CTkEntry(self.root, width=250, show='*', font=("Gill Sans MT", 14), justify='center')
        entry.place(x=640, y=y, anchor='center')
        entry.configure(placeholder_text="Mot de passe", fg_color="black", text_color="#9489ae", placeholder_text_color="#9489ae", corner_radius=0)
        self.add_eye_button(entry, y-7)

    def add_eye_button(self, entry, y):
        eye_img = Image.open("images/oeil.png")
        eye_img.thumbnail((eye_img.width, 13), Image.Resampling.LANCZOS)
        eye_open_image = ImageTk.PhotoImage(eye_img)
        eye_btn = tk.Button(self.root, image=eye_open_image, command=lambda: self.toggle_password_visibility(entry), borderwidth=0, bg='black')
        eye_btn.image = eye_open_image
        eye_btn.place(x=727, y=y)

    def add_buttons(self):
        inscription_button = ctk.CTkButton(self.root, text="Continuer", command=self.open_inscription, fg_color='#2d243f', text_color="#9489ae")
        inscription_button.place(x=640, y=620, anchor='center')

if __name__ == "__main__":
    app = Inscription()

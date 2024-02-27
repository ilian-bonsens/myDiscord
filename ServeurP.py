import os
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class ServeurP:
    def __init__(self):
        self.root = tk.Toplevel()
        self.create_gui() 

    def create_gui(self):
        if self.root is None:
            self.root = tk.Toplevel()
        self.root.title("Discord IML")
        self.root.geometry("640x360")  # Redimensionner la fenêtre
        self.root.configure(bg='black')

        # Charger l'image de fond
        image = Image.open("images/page5.png")

        # Redimensionner l'image
        image = image.resize((640, 360), Image.LANCZOS)  # Redimensionner l'image de fond

        # Convertir l'image PIL en image Tkinter
        self.bg_image = ImageTk.PhotoImage(image)  # Faire de bg_image une variable d'instance

        # Créer un label pour afficher l'image de fond
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Ajouter les barres d'entrée
        self.entry1 = tk.Entry(self.root, width=45, bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 9), justify='center')
        self.entry1.place(x=180, y=110)  # Vous pouvez changer la position ici

        self.entry2 = tk.Entry(self.root, width=30, bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 8), justify='center')
        self.entry2.place(x=228, y=202,)  # Vous pouvez changer la position ici

        # Ajouter le bouton "Continuer"
        self.continue_button = tk.Button(self.root, text="Continuer", padx=20, pady=10, bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 8), command=self.open_chat)
        self.continue_button.place(x=270, y=260)  # Vous pouvez changer la position ici

    def open_chat(self):
        os.system('python3 tchat.py')

# Instancier la classe ServeurP
app = ServeurP()

# Démarrer l'interface utilisateur
tk.mainloop()

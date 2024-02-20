import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.create_main_gui()

    def create_main_gui(self):
        self.root.title("Discord IML")
        self.root.geometry("1280x720")
        self.root.configure(bg='black')

        # Charger l'image de fond
        image = Image.open("images/home.png")

        # Redimensionner l'image
        image = image.resize((1280, 720), Image.LANCZOS)

        # Convertir l'image PIL en image Tkinter
        bg_image = ImageTk.PhotoImage(image)

        # Créer un label pour afficher l'image de fond
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer les boutons pour lancer l'app
        connexion_button = ctk.CTkButton(self.root, text="Démarrer", command=self.connexion, width=250, height=50, corner_radius=0, fg_color='#8a84aa', text_color='#251f3f', font=("Gill Sans MT", 20))
        connexion_button.place(x=640, y=545, anchor='center')

        self.root.mainloop()

    def connexion(self):
        # Importer la classe Connexion du fichier connexion.py
        from connexion import Connexion

        # Créer une instance de la classe Connexion
        connexion = Connexion()

        # Appeler la méthode setup_gui pour afficher le formulaire de connexion
        connexion.create_gui()


if __name__ == "__main__":
    main = Main()
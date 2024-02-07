import customtkinter as ctk
from PIL import Image, ImageTk
from fenetre import Fenetre

class Inscription(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Discord IML - Nouvelle Inscription")
        self.geometry("1280x720")  # Définir la taille de la fenêtre ici

        # Charger l'image de fond et l'ajuster à la fenêtre si nécessaire
        self.load_background_image("images/page2.png")

    def load_background_image(self, filepath):
        # Utiliser PIL pour ouvrir l'image
        background_image = Image.open(filepath)
        
        # Adapter l'image à la taille de la fenêtre si nécessaire
        background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS)

        # Convertir l'image PIL en ImageTk
        background_photo = ImageTk.PhotoImage(background_image)

        # Créer un CTkLabel pour l'image de fond
        label = ctk.CTkLabel(self, image=background_photo)
        label.place(x=0, y=0, width=1280, height=720)

        # Garder une référence à l'image pour éviter le ramassage de l'image par le garbage collector
        self.background_image = background_photo

        # Ajouter d'autres widgets par-dessus l'image de fond ici
        # Par exemple, un bouton :
        button = ctk.CTkButton(self, text="Nom", command=self.on_button_click)
        button.place(x=10, y=10)

    def on_button_click(self):
        print("Le bouton a été cliqué")

# Créer et lancer l'inscription
if __name__ == "__main__":
    app = Inscription()
    app.mainloop()
from PIL import Image, ImageTk
import customtkinter as ctk
from fenetre import Fenetre

def clear_entry(event, entry):
    entry.delete(0, "end")

def create_gui():
    fenetre = Fenetre() # Créer une instance de Fenetre, qui initialise la fenêtre

    # Charger l'image de fond
    image = Image.open("images/page2.png")
    # Redimensionner l'image
    image = image.resize((1280, 720), Image.LANCZOS)
    # Convertir l'image PIL en image Tkinter
    bg_image = ImageTk.PhotoImage(image)

    # Créer un label pour afficher l'image de fond sur fenetre.app
    bg_label = ctk.CTkLabel(fenetre.app, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Créer les champs de saisie pour l'identifiant et le mot de passe sur fenetre.app
    identifiant_entry = ctk.CTkEntry(fenetre.app, width=250, placeholder_text="Identifiant")
    identifiant_entry.place(x=640, y=390, anchor='center')

    mot_de_passe_entry = ctk.CTkEntry(fenetre.app, width=250, show='*')
    mot_de_passe_entry.insert(0, "Mot de passe")
    mot_de_passe_entry.bind("<FocusIn>", lambda event: clear_entry(event, mot_de_passe_entry))
    mot_de_passe_entry.place(x=640, y=450, anchor='center')

    fenetre.app.mainloop()  # Lancer la boucle principale de l'application

if __name__ == "__main__":
    create_gui()
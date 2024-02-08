import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

def clear_entry(event, entry):
    entry.delete(0, tk.END)

def open_inscription():
    # Importer le contenu de inscription.py
    import inscription

def create_gui():
    root = tk.Tk()
    root.title("Discord IML")
    root.geometry("1280x720")
    root.configure(bg='black')

    # Charger l'image de fond
    image = Image.open("images/page2.png")

    # Redimensionner l'image
    image = image.resize((1280, 720), Image.LANCZOS)

    # Convertir l'image PIL en image Tkinter
    bg_image = ImageTk.PhotoImage(image)

    # Créer un label pour afficher l'image de fond
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Définition de la police pour les entrées
    custom_font = ("Gill Sans MT", 14)
    
    # Créer les champs de saisie pour le nom
    nom_entry = ctk.CTkEntry(root, width=250, font=custom_font, justify='center')
    nom_entry.place(x=640, y=300, anchor='center')
    nom_entry.configure(placeholder_text="Nom", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0)

    # Créer les champs de saisie pour le prénom
    prenom_entry = ctk.CTkEntry(root, width=250, font=custom_font, justify='center')
    prenom_entry.place(x=640, y=360, anchor='center')
    prenom_entry.configure(placeholder_text="Prénom", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0)

    # Créer les champs de saisie pour l'email
    email_entry = ctk.CTkEntry(root, width=250, font=custom_font, justify='center')
    email_entry.place(x=640, y=420, anchor='center')
    email_entry.configure(placeholder_text="E-mail", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0)

    # Créer les champs de saisie pour le mot de passe
    mot_de_passe_entry = ctk.CTkEntry(root, width=250, show='*', font=custom_font, justify='center')
    mot_de_passe_entry.place(x=640, y=480, anchor='center')
    mot_de_passe_entry.configure(placeholder_text="Mot de passe", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0)

    # Ajouter un bouton pour Continuer
    inscription_button = ctk.CTkButton(root, text="Continuer", command=open_inscription, fg_color='#2d243f',text_color="#9489ae")
    inscription_button.place(x=640, y=620, anchor='center')
    
   # Créer un Canvas pour la croix à l'emplacement désiré
    canvas_cross = tk.Canvas(root, width=24, height=24, bg='#2d243f', highlightthickness=0)
    canvas_cross.place(x=423, y=543)  # Ajustez si nécessaire pour l'emplacement exact

    # Identifiant pour les éléments de la croix sur le canvas
    cross_elements = None

    # Fonction pour afficher/cacher la croix
    def toggle_cross(event):
        nonlocal cross_elements
        if cross_elements:
            # Si la croix est déjà affichée, supprimer les éléments
            canvas_cross.delete("cross")
            cross_elements = None
        else:
            # Si la croix n'est pas affichée, la dessiner
            canvas_cross.create_line(0, 0, 25, 25, fill='#9489ae', width=2, tags="cross")
            canvas_cross.create_line(0, 25, 25, 0, fill='#9489ae', width=2, tags="cross")
            cross_elements = True  # Mettre à jour l'indicateur

    # Lie l'événement de clic à la zone où la croix doit apparaître/disparaître
    canvas_cross.bind("<Button-1>", toggle_cross)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
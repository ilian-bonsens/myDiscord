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
    image = Image.open("images/page1.png")

    # Redimensionner l'image
    image = image.resize((1280, 720), Image.LANCZOS)

    # Convertir l'image PIL en image Tkinter
    bg_image = ImageTk.PhotoImage(image)

    # Créer un label pour afficher l'image de fond
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Créer les champs de saisie pour l'identifiant et le mot de passe
    identifiant_entry = ctk.CTkEntry(root, width=250, justify="center")
    identifiant_entry.place(x=640, y=390, anchor='center')
    identifiant_entry.configure(placeholder_text="Identifiant", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MTç", 12))



    mot_de_passe_entry = ctk.CTkEntry(root, width=250, show='*', justify="center")
    mot_de_passe_entry.place(x=640, y=450, anchor='center')
    mot_de_passe_entry.configure(placeholder_text="Mot de passe", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MT", 12))

    # Ajouter un label "Pas encore inscrit ?"
    inscription_label = tk.Label(root, text="Pas encore inscrit ?", bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 12))
    inscription_label.place(x=640, y=490, anchor='center')

    # Ajouter un bouton pour ouvrir la page d'inscription
    inscription_button = ctk.CTkButton(root, text="Inscription", command=open_inscription, fg_color='#2d243f',text_color="#9489ae", font=("Gill Sans MT", 18))
    inscription_button.place(x=640, y=520, anchor='center')

    root.mainloop()

if __name__ == "__main__":
    create_gui()

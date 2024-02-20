import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class Connexion:
    def __init__(self):
        self.root = tk.Toplevel()
        self.create_gui()

    def clear_entry(self, event, entry):
        entry.delete(0, tk.END)

    def tchat(self): # lorsque l'on clique sur le bouton connexion, cela renvoie à la page d'accueil
        # Importer le contenu de tchat.py
        from tchat import Tchat

        # Créer une instance de la classe tchat
        tchat = Tchat()

        # Appeler la méthode create_gui pour afficher la page d'accueil
        tchat.create_gui

    # Modifiez la signature de la fonction pour accepter l'entry comme argument
    def toggle_password_visibility(self, entry):
        if entry.cget('show') == '*':
            entry.configure(show='')
        else:
            entry.configure(show='*')

    def inscription(self, event):
        # Importer la classe Inscription du fichier inscription.py
        from inscription import Inscription

        # Créer une instance de la classe Inscription
        inscription = Inscription()

        # Appeler la méthode setup_gui pour afficher le formulaire d'inscription
        inscription.setup_gui()

    def create_gui(self):
        self.root.title("Discord IML")
        self.root.geometry("1280x720")
        self.root.configure(bg='black')

        # Charger l'image de fond
        image = Image.open("images/page1.png")

        # Redimensionner l'image
        image = image.resize((1280, 720), Image.LANCZOS)

        # Convertir l'image PIL en image Tkinter
        bg_image = ImageTk.PhotoImage(image)

        # Créer un label pour afficher l'image de fond
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer les champs de saisie pour l'identifiant et le mot de passe
        identifiant_entry = ctk.CTkEntry(self.root, width=250, justify="center")
        identifiant_entry.place(x=640, y=390, anchor='center')
        identifiant_entry.configure(placeholder_text="Identifiant", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MTç", 12))

        mot_de_passe_entry = ctk.CTkEntry(self.root, width=250, show='*', justify="center")
        mot_de_passe_entry.place(x=640, y=450, anchor='center')
        mot_de_passe_entry.configure(placeholder_text="Mot de passe", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MT", 12))

        # Charger et redimensionner l'image de l'œil
        eye_img = Image.open("images/oeil.png")
        eye_img.thumbnail((eye_img.width, 13), Image.Resampling.LANCZOS)
        eye_open_image = ImageTk.PhotoImage(eye_img)

        # Créer un bouton pour afficher/masquer le mot de passe
        # Utilisez une fonction lambda pour passer mot_de_passe_entry en argument
        eye_btn = tk.Button(self.root, image=eye_open_image, command=lambda: self.toggle_password_visibility(mot_de_passe_entry), borderwidth=0, bg='black')
        eye_btn.image = eye_open_image  # Gardez une référence de l'image pour éviter le ramasse-miettes
        eye_btn.place(x=727, y=443)  # Ajustez si nécessaire pour l'emplacement exact

        # Ajouter un bouton pour ouvrir la page d'inscription
        connexion_button = ctk.CTkButton(self.root, text="Connexion", command=self.tchat, fg_color='#2d243f',text_color="#9489ae", font=("Gill Sans MT", 18))
        connexion_button.place(x=640, y=500, anchor='center')

        # Ajouter un label "Pas encore inscrit ?"
        inscription_label = tk.Label(self.root, text="Pas encore inscrit ?", bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 12))
        inscription_label.place(x=640, y=575, anchor='center')

        # Lier un événement de clic de souris au label
        inscription_label.bind("<Button-1>", self.inscription)

        self.root.mainloop()

if __name__ == "__main__":
    app = Connexion()

import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import mysql.connector
import hashlib, os

class Inscription:
    def __init__(self):
        self.root = tk.Tk()  # ligne remplacée
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

        self.entries = {
            "nom": self.create_entry("Nom", 300),
            "prenom": self.create_entry("Prénom", 360),
            "email": self.create_entry("E-mail", 420),
            "password": self.create_password_entry(480)
        }

        self.add_buttons()

        self.root.mainloop()

    def create_entry(self, placeholder, y):
        entry = ctk.CTkEntry(self.root, width=250, font=("Gill Sans MT", 14), justify='center')
        entry.place(x=640, y=y, anchor='center')
        entry.configure(placeholder_text=placeholder, fg_color="black", text_color="#9489ae", placeholder_text_color="#9489ae", corner_radius=0)
        return entry

    def create_password_entry(self, y):
        entry = ctk.CTkEntry(self.root, width=250, show='*', font=("Gill Sans MT", 14), justify='center')
        entry.place(x=640, y=y, anchor='center')
        entry.configure(placeholder_text="Mot de passe", fg_color="black", text_color="#9489ae", placeholder_text_color="#9489ae", corner_radius=0)
        self.add_eye_button(entry, y-7)
        return entry

    def add_eye_button(self, entry, y):
        eye_img = Image.open("images/oeil.png")
        eye_img.thumbnail((eye_img.width, 13), Image.Resampling.LANCZOS)
        eye_open_image = ImageTk.PhotoImage(eye_img)
        eye_btn = tk.Button(self.root, image=eye_open_image, command=lambda: self.toggle_password_visibility(entry), borderwidth=0, bg='black')
        eye_btn.image = eye_open_image
        eye_btn.place(x=727, y=y)

    def add_buttons(self):
        inscription_button = ctk.CTkButton(self.root, text="Continuer", command=lambda: [self.connexion() if self.save_user_to_database() else None], fg_color='#2d243f', text_color="#9489ae")
        inscription_button.place(x=640, y=620, anchor='center')

    def save_user_to_database(self):
        # Collecter les données des entrées
        nom = self.entries["nom"].get()
        prenom = self.entries["prenom"].get()
        email = self.entries["email"].get()
        password = self.entries["password"].get()

        if not nom or not prenom or not email or not password:
            print("Veuillez remplir tous les champs")
            return False
    
        salt = os.urandom(16)
        hashed_password = hashlib.sha384((password + salt.hex()).encode()).hexdigest()

        # Connexion à la base de données
        try:
            conn = mysql.connector.connect(host='localhost', database='Discord', user='root', password='AscZdvEfb520.+SQL')
            cursor = conn.cursor()
            query = "INSERT INTO utilisateurs (nom, prenom, mail, mot_de_passe, sel) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nom, prenom, email, hashed_password, salt.hex()))
            conn.commit()
            print("Utilisateur ajouté avec succès")
            return True
        except mysql.connector.Error as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def connexion(self):
        self.root.destroy()
        # Importer la classe Connexion du fichier connexion.py
        from connexion import Connexion

        # Créer une instance de la classe Connexion
        connexion = Connexion()

        # Appeler la méthode setup_gui pour afficher le formulaire de connexion
        connexion.create_gui()        
    
if __name__ == "__main__":
    app = Inscription()
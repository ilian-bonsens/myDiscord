import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import mysql.connector, hashlib

class Connexion:
    prenom = None  # Définir prenom comme une variable de classe

    def __init__(self):
        self.root = tk.Tk()
        self.create_gui()

    def clear_entry(self, event, entry):
        entry.delete(0, tk.END)

    def tchat(self): 
        # Récupérer les informations d'identification de l'utilisateur
        identifiant = self.identifiant_entry.get()
        password = self.mot_de_passe_entry.get()

        # Vérifier si l'utilisateur existe
        if self.check_user(identifiant, password):
            self.root.destroy()
            # Importer le contenu de tchat.py
            from tchat import Tchat
            # Créer une instance de la classe tchat
            tchat = Tchat()
            # Appeler la méthode create_gui pour afficher la page d'accueil
            tchat.create_gui()
        else:
            print("Identifiant ou mot de passe incorrect")

    # Modifiez la signature de la fonction pour accepter l'entry comme argument
    def toggle_password_visibility(self, entry):
        if entry.cget('show') == '*':
            entry.configure(show='')
        else:
            entry.configure(show='*')

    def inscription(self, event):
        self.root.destroy()
        # Importer la classe Inscription du fichier inscription.py
        from inscription import Inscription

        # Créer une instance de la classe Inscription
        inscription = Inscription()

        # Appeler la méthode setup_gui pour afficher le formulaire d'inscription
        inscription.setup_gui()

    def check_user(self, mail, password):
        try:
            conn = mysql.connector.connect(host='localhost', database='Discord', user='root', password='mars1993')
            cursor = conn.cursor()
            query = "SELECT prenom, mot_de_passe, sel FROM utilisateurs WHERE mail = %s"
            cursor.execute(query, (mail,))
            result = cursor.fetchone() # Récupère la première ligne de résultat
            if result is None:
                print("Mail incorrect")
                return False  # Retourne False si aucun utilisateur trouvé
            else:
                self.prenom, stored_password, sel = result
                Connexion.prenom = self.prenom  # Mettre à jour la variable de classe
                # Hash the user's password with the stored salt
                hashed_password = hashlib.sha384((password + sel).encode()).hexdigest()
                if hashed_password == stored_password:
                    print("Connexion réussie")
                    print(f"Bienvenue {Connexion.prenom}")
                    return True  # Retourne True si l'utilisateur est trouvé
                else:
                    print("Mot de passe incorrect")
                    return False
        except mysql.connector.Error as e:
            print(f"Erreur lors de la vérification dans la base de données: {e}")
            return False  # En cas d'erreur, retourne False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def create_gui(self):
        if self.root is None:
            self.root = tk.Tk()
        self.root.title("Discord IML")
        self.root.geometry("1280x720")
        self.root.configure(bg='black')
        self.identifiant_entry = ctk.CTkEntry(self.root, width=250, justify="center")
        self.mot_de_passe_entry = ctk.CTkEntry(self.root, width=250, show='*', justify="center")

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
        self.identifiant_entry = ctk.CTkEntry(self.root, width=250, justify="center")
        self.identifiant_entry.place(x=640, y=390, anchor='center')
        self.identifiant_entry.configure(placeholder_text="Identifiant", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MTç", 12))

        self.mot_de_passe_entry = ctk.CTkEntry(self.root, width=250, show='*', justify="center")
        self.mot_de_passe_entry.place(x=640, y=450, anchor='center')
        self.mot_de_passe_entry.configure(placeholder_text="Mot de passe", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MT", 12))

        # Charger et redimensionner l'image de l'œil
        eye_img = Image.open("images/oeil.png")
        eye_img.thumbnail((eye_img.width, 13), Image.Resampling.LANCZOS)
        eye_open_image = ImageTk.PhotoImage(eye_img)

        # Créer un bouton pour afficher/masquer le mot de passe
        # Utilisez une fonction lambda pour passer mot_de_passe_entry en argument
        eye_btn = tk.Button(self.root, image=eye_open_image, command=lambda: self.toggle_password_visibility(self.mot_de_passe_entry), borderwidth=0, bg='black')
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
import tkinter as tk
import customtkinter as ctk
import datetime as dt
import mysql.connector
import emoji
from PIL import Image, ImageTk
from connexion import Connexion

class Tchat(Connexion):
    def __init__(self):
        self.custom_font = ("Gill Sans MT", 16)
        self.emoji_font = ("Segoe UI Emoji", 18)
        self.labels = []
        self.ami = 0
        super().__init__()  # Initialise la classe parente en premier
        self.root = tk.Tk()
        self.y_position = 350
        self.emoji_fenetre = None
        self.create_gui()  # Crée l'interface utilisateur après l'initialisation de la classe parente

    def clear_entry(self, event, entry):
        entry.delete(0, tk.END)

    def create_gui(self):
        self.root.title("Discord IML")
        self.root.geometry("1280x720")

        # Charger l'image de fond
        image = Image.open("images/page3.png")
        button_image = Image.open("images/add.png")
        deco_image = Image.open("images/deconnexion.png")

        # Redimensionner l'image
        image = image.resize((1280, 720), Image.LANCZOS)
        button_image = button_image.resize((55, 55), Image.LANCZOS)
        deco_image = deco_image.resize((45, 45), Image.LANCZOS)

        # Convertir l'image PIL en image Tkinter
        self.bg_image = ImageTk.PhotoImage(image)
        tk_image = ImageTk.PhotoImage(button_image)
        deco_image = ImageTk.PhotoImage(deco_image)

        # Créer un label pour afficher l'image de fond
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer un bouton pour les amis
        button_friends = tk.Button(self.root, image=tk_image, borderwidth=0, highlightthickness=0, command=self.ajouter_ami)
        button_friends.image = tk_image  # Gardez une référence à l'image
        button_friends.place(x=255, y=140, anchor='nw')  # Modifiez les coordonnées x et y si nécessaire
        button_friends.configure(bg='#2d243f')

        # Créer un bouton pour les groupes
        button_groups = tk.Button(self.root, image=tk_image, borderwidth=0, highlightthickness=0)
        button_groups.image = tk_image  # Gardez une référence à l'image
        button_groups.place(x=20, y=140, anchor='nw')  # Modifiez les coordonnées x et y si nécessaire
        button_groups.configure(bg='#2d243f')

        #Créer une frame qui contiendra les widgets de la conversation
        frame = ctk.CTkFrame(self.root)
        frame.grid(row=0, column=0, padx=470, pady=(150, 0), sticky="nsw")
        frame.configure(width=780, height=470, fg_color='black', corner_radius=0)

        # Créer un CTkScrollableFrame à l'intérieur du CTkFrame
        self.interior_frame = ctk.CTkScrollableFrame(frame)
        self.interior_frame.configure(width=660, height=390, fg_color='black', corner_radius=0)
        self.interior_frame.place(x=80, y=10, anchor='nw')  # Modifiez les coordonnées x et y

        self.chat_entry = ctk.CTkEntry(self.root, width=610, height=35)
        self.chat_entry.place(x=550, y=565, anchor='nw')
        self.chat_entry.configure(font=self.custom_font, fg_color='grey30', text_color='white', corner_radius=0, placeholder_text='Envoyer un message à @')

        self.chat_entry.bind("<Return>", self.update_label)

        # Créer un bouton pour des emojis
        button_emojis = tk.Button(self.root, image=tk_image, command=self.insert_emoji, borderwidth=0, highlightthickness=0)
        button_emojis.image = tk_image  # Gardez une référence à l'image
        button_emojis.place(x=1128, y=570, anchor='nw')
        button_emojis.configure(bg='#2d243f', width=25, height=25)

        # Charger et redimensionner l'image du téléphone
        phone_image = Image.open("images/telephone.png")  # Assurez-vous que le chemin est correct
        phone_image = phone_image.resize((30, 30), Image.Resampling.LANCZOS)  # Redimensionner selon vos besoins
        phone_photo = ImageTk.PhotoImage(phone_image)

        # Créer le bouton du téléphone en bas à droite
        phone_button = tk.Button(self.root, image=phone_photo, bg='black', borderwidth=0, highlightthickness=0)
        phone_button.image = phone_photo  # Gardez une référence
        phone_button.place(relx=1.0, rely=1.0, anchor='se', x=-65, y=-123) # Ajustez selon vos besoins

        # Créer un bouton deconnexion
        button_deco = tk.Button(self.root, image=deco_image, command=self.deconnexion, borderwidth=0, highlightthickness=0)
        button_deco.image = deco_image  # Gardez une référence à l'image
        button_deco.place(x=1210, y=660, anchor='nw')
        button_deco.configure(bg='#2d243f', width=45, height=45)

        self.root.mainloop()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def ajouter_ami(self):
        # Crée une nouvelle fenêtre
        self.ami_window = tk.Toplevel(self.root)
        self.ami_window.title("Ajouter un ami")
        self.ami_window.geometry("500x250")
        self.ami_window.configure(bg='#2d243f')
        self.ami_window.label = ctk.CTkLabel(self.ami_window, text="Ajouter un ami", font=("Gill Sans MT", 40), text_color='#9489ae')
        self.ami_window.label.place(x=250, y=70, anchor='center')  # Coordonnées x et y du texte
        self.ami_window.entry = ctk.CTkEntry(self.ami_window, width=250, height=35, placeholder_text="Entrez le prenom de l'ami à ajouter")
        self.ami_window.entry.place(x=250, y=150, anchor='center') # Coordonnées x et y du champ de saisie

        # Dictionnaire associant les noms d'amis à des chemins d'images
        ami_image_paths = {
            'Marion': 'images/icone_m.png',
            'Lucas': 'images/icone_l.png',
            'Ilian': 'images/icone_i.png',
        }

        def on_return(event):
            ami = self.ami_window.entry.get() 
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    database="Discord",
                    password="AscZdvEfb520.+SQL"
                )
            print("Connecté à la base de données")  # Ajouté pour le débogage

            mycursor = mydb.cursor()

            # Vérifie si le destinataire existe dans la base de données
            sql = "SELECT * FROM utilisateurs WHERE prenom = %s"
            mycursor.execute(sql, (ami,))
            result = mycursor.fetchone()
            if result is None:
                print("Erreur : l'utilisateur n'existe pas.")
            else:
                print("Utilisateur ajouté.")
                self.ami += 1
                self.ami_window.destroy()
                # Créer un bouton pour l'ami ajouté
                path = ami_image_paths.get(ami, 'images/add.png')
                button_image = Image.open(path)
                button_image = button_image.resize((55, 55), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(button_image)
                button_friends = tk.Button(self.root, image=tk_image, borderwidth=0, highlightthickness=0)
                button_friends.image = tk_image  # Gardez une référence à l'image
                button_friends.place(x=255, y=140 + 70 * self.ami, anchor='nw')  # Modifiez les coordonnées x et y en fonction du nombre d'amis
                button_friends.configure(bg='#2d243f', width=55, height=55)

        self.ami_window.entry.bind("<Return>", on_return)

    def update_label(self, event):
        message = self.chat_entry.get()
        now = dt.datetime.now()
        date_time = now.strftime('%Y-%m-%d %H:%M:%S')
        if len(message) > 0 and message[0] == '@':
            destinataire, message = message.split(' ', 1)
            destinataire = destinataire[1:]  # Enlève le '@' du début
            self.chat_entry.delete(0, len(message))
            for label in self.labels:
                label.pack(side='top')  # Ajoute le label au haut de l'affichage
            label = ctk.CTkLabel(self.interior_frame)  # Ajoutez le label à interior_frame
            label.configure(font=self.custom_font, fg_color='black', text_color='#9489ae', wraplength=610, justify='left', text=f'{Connexion.prenom} : {message} ({date_time})')
            label.pack(anchor='w', padx=5, pady=5)  # Ajoute le nouveau label à gauche avec un padding de 10 pixels
            self.labels.append(label)
            self.root.update_idletasks()  # Mettez à jour l'interface utilisateur
            self.message_database(message, date_time, destinataire)  # Appel à la méthode pour enregistrer le message dans la base de données

    def on_close(self):
        self.root.destroy()

    def insert_emoji(self):
        # Crée une nouvelle fenêtre
        self.emoji_window = tk.Toplevel(self.root)
        self.emoji_window.title("Choisir un emoji")
        self.emoji_window.geometry("287x50")
        
        # Crée une liste d'emojis
        emojis = ['\U0001F600', '\U0001F605', '\U0001F602', '\U0001F633', '\U0001F9D0', '\U0001F60D', '\U0001F972', '\U0001F910']

        # Crée un bouton pour chaque emoji
        for i, e in enumerate(emojis):
            button = tk.Button(self.emoji_window, text=emoji.emojize(e), command=lambda e=e: self.on_emoji_click(e), height=1, width=2)
            button['font'] = ("Segoe UI Emoji", 18)
            button.grid(row=i//10, column=i%10)  # Arrange les boutons en une grille de 10x10

    def on_emoji_click(self, e):
        # Insère l'emoji dans le champ de texte
        self.chat_entry.insert(tk.END, emoji.emojize(e))
        self.chat_entry.configure(font=self.emoji_font)

    def message_database(self, message, date_time, destinataire):
        # Enregistrement du message dans la base de données
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="Discord",
                password="AscZdvEfb520.+SQL"
            )
            print("Connecté à la base de données")  # Ajouté pour le débogage

            mycursor = mydb.cursor()

            # Vérifie si le destinataire existe dans la base de données
            sql = "SELECT * FROM utilisateurs WHERE prenom = %s"
            mycursor.execute(sql, (destinataire,))
            result = mycursor.fetchone()
            if result is None:
                print("Erreur : l'utilisateur n'existe pas.")
                return

            contenu = message
            date_heure = date_time
            utilisateur = Connexion.prenom

            # Insertion du message dans la base de données
            sql = "INSERT INTO messages (utilisateur, date_heure, contenu, destinataire) VALUES (%s, %s, %s, %s)"
            if hasattr(self, 'prenom'): # Vérifie si l'attribut prenom existe
                print(f'Nouveau message de {Connexion.prenom}')
            # Exécution de la requête
            mycursor.execute(sql, (utilisateur, date_heure, contenu, destinataire))
            mydb.commit()
            print("Message enregistré")  # Ajouté pour le débogage
            
        # Gestion des erreurs
        except mysql.connector.Error as err:
            print("Une erreur MySQL s'est produite :", err)
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

    def deconnexion(self):
        self.root.destroy()
        # Importer la classe Connexion du fichier connexion.py
        from connexion import Connexion

        # Créer une instance de la classe Connexion
        connexion = Connexion()

        # Appeler la méthode setup_gui pour afficher le formulaire de connexion
        connexion.create_gui() 

if __name__ == "__main__":
    app = Tchat()
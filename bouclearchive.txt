import tkinter as tk
import customtkinter as ctk
from inscription import Inscription
from connexion import Connexion

class Fenetre:
    def __init__(self):
        self.app = ctk.CTk()
        self.framerate = 60
        self.app.title("Discord IML")
        self.app.geometry("1280x720")
        self.app.iconbitmap('images/discord-icon.ico')

        self.etat = "connexion"  # Initialiser l'état de la fenêtre
        self.run()  # Lancer la boucle principale

    def run(self):
        while True:
            if self.etat == "connexion":
                connexion = Connexion(self.app)
                self.etat = connexion.run()
            elif self.etat == "inscription":
                inscription = Inscription(self.app)
                self.etat = inscription.run()
            elif self.etat == "quitter":
                break

if __name__ == "__main__":
    fenetre = Fenetre()

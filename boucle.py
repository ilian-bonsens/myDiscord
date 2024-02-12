import tkinter as tk
import customtkinter as ctk
from fenetre import Fenetre
from inscription import Inscription

class Boucle:
    def __init__(self):
        # Initialisation de l'interface graphique Tkinter
        self.root = tk.Tk()
        self.fenetre = Fenetre()
        self.etat = "menu"

    def run(self):
        while True:
            #noms des fichiers et class à changer pour code de lucas
            if self.etat == "menu":
                menu = Menu(self.fenetre.ecran)
                self.etat = menu.run()
            #transition marion
            elif self.etat == "inscription":
                inscription = Inscription(self.fenetre.ecran)
                self.etat = inscription.run()
            elif self.etat == "quitter":
                break

if __name__ == "__main__":
    chat = Boucle()
    chat.run()
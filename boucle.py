import tkinter as tk
import customtkinter as ctk
from inter1 import 

class Boucle:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.fenetre = Fenetre()
        self.etat = "menu"

    def run(self):
        while True:
            if self.etat == "menu":
                menu = Menu(self.fenetre.ecran)
                self.etat = menu.run()
            elif self.etat == "personnage":
                personnage = Personnage(self.fenetre.ecran)
                self.etat = personnage.run()
            elif self.etat == "choixpokemon":
                choix_pokemon = ChoixPokemon(self.fenetre.ecran)
                self.etat = choix_pokemon.run()
            elif self.etat == "quitter":
                break
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()

if __name__ == "__main__":
    chat = Boucle()
    chat.run()
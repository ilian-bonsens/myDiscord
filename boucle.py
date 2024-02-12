import tkinter as tk
import customtkinter as ctk
from fenetre import Fenetre
from import
from inscription import Inscription
from import

class Boucle:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
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
            #noms des fichiers et class a changer pour transition vers code d'ilian
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

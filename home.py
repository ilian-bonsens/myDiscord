import tkinter as tk
from PIL import Image, ImageTk
from fenetre import Fenetre

def background(fenetre):
    # Charger l'image de fond
    image = Image.open("images/home.png")
    fenetre = Fenetre()
    fenetre.mainloop()
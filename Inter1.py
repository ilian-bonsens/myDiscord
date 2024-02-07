import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

def clear_entry(event, entry):
    entry.delete(0, tk.END)

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
    identifiant_entry = ctk.CTkEntry(root, width=250)
    identifiant_entry.insert(0, "Identifiant")
    identifiant_entry.bind("<FocusIn>", lambda event: clear_entry(event, identifiant_entry))
    identifiant_entry.place(x=640, y=390, anchor='center')

    mot_de_passe_entry = ctk.CTkEntry(root, width=250, show='*')
    mot_de_passe_entry.insert(0, "Mot de passe")
    mot_de_passe_entry.bind("<FocusIn>", lambda event: clear_entry(event, mot_de_passe_entry))
    mot_de_passe_entry.place(x=640, y=450, anchor='center')

    root.mainloop()

if __name__ == "__main__":
    create_gui()

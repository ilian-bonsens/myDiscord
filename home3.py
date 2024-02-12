import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import datetime as dt

custom_font = ("Gill Sans MT", 13)

def clear_entry(event, entry):
    entry.delete(0, tk.END)

def create_gui():
    root = tk.Tk()
    root.title("Discord IML")
    root.geometry("1280x720")

    # Charger l'image de fond
    image = Image.open("images/home.png")

    # Redimensionner l'image
    image = image.resize((1280, 720), Image.LANCZOS)

    # Convertir l'image PIL en image Tkinter
    bg_image = ImageTk.PhotoImage(image)

    # Créer un label pour afficher l'image de fond
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    #Créer une frame qui contiendra les widgets de la conversation
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=470, pady=(150, 0), sticky="nsw")
    frame.configure(width=780, height=470, fg_color='grey20', corner_radius=0)

    # Créer un CTkScrollableFrame à l'intérieur du CTkFrame
    interior_frame = ctk.CTkScrollableFrame(frame)
    interior_frame.configure(width=660, height=390, fg_color='grey20', corner_radius=0)
    interior_frame.place(x=80, y=10, anchor='nw')  # Modifiez les coordonnées x et y

    chat_entry = ctk.CTkEntry(root, width=610, height=35)
    chat_entry.place(x=550, y=565, anchor='nw')
    chat_entry.configure(font=custom_font, fg_color='grey30', text_color='white', corner_radius=0, placeholder_text='Envoyer un message à @')

    labels = []
    y_position = 350

    def update_label(event):
        nonlocal y_position
        message = chat_entry.get()
        now = dt.datetime.now()
        date_time = now.strftime('%H:%M:%S')
        if len(message) > 0:
            chat_entry.delete(0, len(message))
            for label in labels:
                label.pack(side='top')  # Ajoute le label au haut de l'affichage
            label = ctk.CTkLabel(interior_frame)  # Ajoutez le label à interior_frame
            label.configure(font=custom_font, fg_color='grey21', text_color='white', wraplength=610, justify='left', text=f'{message} ({date_time})')
            label.pack(anchor='w', padx=10, pady=10)  # Ajoute le nouveau label à gauche avec un padding de 10 pixels
            labels.append(label)
            root.update_idletasks()  # Mettez à jour l'interface utilisateur

    chat_entry.bind("<Return>", update_label)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
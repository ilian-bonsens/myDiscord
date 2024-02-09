import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

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
    scrollable_frame = ctk.CTkScrollableFrame(root)
    scrollable_frame.grid(row=0, column=0, padx=470, pady=(150, 0), sticky="nsw")
    scrollable_frame.configure(width=780, height=470, fg_color='grey20', corner_radius=0)

    chat_entry = ctk.CTkEntry(root, width=650, height=35)
    chat_entry.place(x=540, y=565, anchor='nw')
    chat_entry.configure(fg_color='grey30', text_color='white', corner_radius=0, placeholder_text='Envoyer un message à @')

    labels = []
    y_position = 510

    def update_label(event):
        nonlocal y_position
        message = chat_entry.get()
        if len(message) > 0:
            chat_entry.delete(0, len(message))
            for label in labels:
                y = int(label.place_info()['y'])
                label.place(x=540, y=y-50)  # déplace chaque label existant de 20 pixels vers le haut
            label = ctk.CTkLabel(root)
            label.place(x=540, y=y_position, anchor='nw')
            label.configure(fg_color='grey21', text_color='white', text=message)
            labels.append(label)
            root.update_idletasks()  # Mettez à jour l'interface utilisateur

    chat_entry.bind("<Return>", update_label)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
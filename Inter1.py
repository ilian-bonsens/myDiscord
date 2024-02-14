import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class Inter:
    @staticmethod
    def clear_entry(event, entry):
        entry.delete(0, tk.END)

    @staticmethod
    def open_inscription():
        import inscription

    @staticmethod
    def toggle_password_visibility(entry):
        if entry.cget('show') == '*':
            entry.configure(show='')
        else:
            entry.configure(show='*')

    def create_gui(self):
        root = tk.Tk()
        root.title("Discord IML")
        root.geometry("1280x720")
        root.configure(bg='black')

        image = Image.open("images/page1.png")
        image = image.resize((1280, 720), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        identifiant_entry = ctk.CTkEntry(root, width=250, justify="center")
        identifiant_entry.place(x=640, y=390, anchor='center')
        identifiant_entry.configure(placeholder_text="Identifiant", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MTç", 12))

        mot_de_passe_entry = ctk.CTkEntry(root, width=250, show='*', justify="center")
        mot_de_passe_entry.place(x=640, y=450, anchor='center')
        mot_de_passe_entry.configure(placeholder_text="Mot de passe", fg_color="black",text_color="#9489ae",placeholder_text_color="#9489ae", corner_radius=0, font=("Gill Sans MT", 12))

        eye_img = Image.open("images/oeil.png")
        eye_img.thumbnail((eye_img.width, 13), Image.Resampling.LANCZOS)
        eye_open_image = ImageTk.PhotoImage(eye_img)

        eye_btn = tk.Button(root, image=eye_open_image, command=lambda: self.toggle_password_visibility(mot_de_passe_entry), borderwidth=0, bg='black')
        eye_btn.image = eye_open_image
        eye_btn.place(x=727, y=443)

        inscription_label = tk.Label(root, text="Pas encore inscrit ?", bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 12))
        inscription_label.place(x=640, y=490, anchor='center')

        inscription_button = ctk.CTkButton(root, text="Inscription", command=self.open_inscription, fg_color='#2d243f',text_color="#9489ae", font=("Gill Sans MT", 18))
        inscription_button.place(x=640, y=520, anchor='center')

        root.mainloop()

if __name__ == "__main__":
    Inter().create_gui()

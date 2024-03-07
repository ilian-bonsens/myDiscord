import os
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import datetime as dt
import mysql.connector
from connexion import Connexion
import emoji
from plyer import notification

class ServeurP:
    def __init__(self):
        self.custom_font = ("Gill Sans MT", 16)
        self.emoji_font = ("Segoe UI Emoji", 18)
        self.labels = []
        self.root = tk.Tk()
        self.y_position = 350
        self.emoji_fenetre = None
        self.last_update = dt.datetime(2000, 1, 1)
        self.create_Serveur()

    def clear_entry(self, event, entry):
        entry.delete(0, tk.END)

    def create_Serveur(self):
        self.root.title("Discord IML")
        self.root.geometry("1280x720")
        self.root.configure(bg='black')

        image = Image.open("images/page7.png")
        image = image.resize((1280, 720), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame = ctk.CTkFrame(self.root)
        frame.grid(row=0, column=0, padx=470, pady=(150, 0), sticky="nsw")
        frame.configure(width=780, height=470, fg_color='black', corner_radius=0)

        self.interior_frame = ctk.CTkScrollableFrame(frame)
        self.interior_frame.configure(width=660, height=390, fg_color='black', corner_radius=0)
        self.interior_frame.place(x=80, y=10, anchor='nw')

        serveurs = self.get_new_serveurs()

        for utilisateur, date_heure, contenu in serveurs:
            label = ctk.CTkLabel(self.interior_frame)
            label.configure(font=self.custom_font, fg_color='black', text_color='#9489ae', wraplength=610, justify='left', text=f'{utilisateur} : {contenu} ({date_heure})')
            label.pack(anchor='w', padx=5, pady=5)
            self.labels.append(label)

        self.Serveur_entry = ctk.CTkEntry(self.root, width=610, height=35)
        self.Serveur_entry.place(x=550, y=565, anchor='nw')
        self.Serveur_entry.configure(font=self.custom_font, fg_color='grey30', text_color='white', corner_radius=0, placeholder_text='Envoyer un message à @')

        self.Serveur_entry.bind("<Return>", self.update_label)

        self.continue_button = tk.Button(self.root, text="Retour", padx=20, pady=10, bg='#9489ae', fg='#2d243f', font=("Gill Sans MT", 10), command=self.open_chat)
        self.continue_button.place(x=1150, y=657)

        image = Image.open("images/page7.png")
        button_image = Image.open("images/add.png")
        image = image.resize((1280, 720), Image.LANCZOS)
        button_image = button_image.resize((55, 55), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        tk_image = ImageTk.PhotoImage(button_image)

        button_emojis = tk.Button(self.root, image=tk_image, command=self.insert_emoji, borderwidth=0, highlightthickness=0)
        button_emojis.image = tk_image
        button_emojis.place(x=1128, y=570, anchor='nw')
        button_emojis.configure(bg='#2d243f', width=25, height=25)

        self.root.after(2000, self.update_messages)
        self.root.mainloop()

    def update_messages(self):
        serveurs = self.get_new_serveurs()

        for utilisateur, date_heure, contenu in serveurs:
            label = ctk.CTkLabel(self.interior_frame)
            label.configure(font=self.custom_font, fg_color='black', text_color='#9489ae', wraplength=610, justify='left', text=f'{utilisateur} : {contenu} ({date_heure})')
            label.pack(anchor='w', padx=5, pady=5)
            self.labels.append(label)

        self.root.after(2000, self.update_messages)

    def on_close(self):
        self.root.destroy()

    def update_label(self, event):
        message = self.Serveur_entry.get()
        now = dt.datetime.now()
        date_time = now.strftime('%Y-%m-%d %H:%M:%S')
        if len(message) > 0:
            self.Serveur_entry.delete(0, len(message))
            self.message_database(message, date_time)

            notification.notify(
                title='Nouveau message',
                message=f'{Connexion.prenom} a envoyé un message',
                timeout=10
            )

    def insert_emoji(self):
        self.emoji_window = tk.Tk(self.root)
        self.emoji_window.title("Choisir un emoji")
        self.emoji_window.geometry("287x50")

        emojis = ['\U0001F600', '\U0001F605', '\U0001F602', '\U0001F633', '\U0001F9D0', '\U0001F60D', '\U0001F972', '\U0001F910']

        for i, e in enumerate(emojis):
            button = tk.Button(self.emoji_window, text=emoji.emojize(e), command=lambda e=e: self.on_emoji_click(e), height=1, width=2)
            button['font'] = ("Segoe UI Emoji", 18)
            button.grid(row=i//10, column=i%10)

    def on_emoji_click(self, e):
        self.Serveur_entry.insert(tk.END, emoji.emojize(e))
        self.Serveur_entry.configure(font=self.emoji_font)

    def message_database(self, message, date_time):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="Discord",
                password="AscZdvEfb520.+SQL"
            )

            mycursor = mydb.cursor()

            contenu = message
            date_heure = date_time
            utilisateur = Connexion.prenom

            sql = "INSERT INTO serveurs (utilisateur, date_heure, contenu) VALUES (%s, %s, %s)"
            val = (utilisateur, date_heure, contenu)

            mycursor.execute(sql, val)
            mydb.commit()

            print(f'Nouveau message de {utilisateur} enregistré dans la base de données')

        except mysql.connector.Error as err:
            print("Une erreur MySQL s'est produite :", err)
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

    def get_new_serveurs(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="Discord",
                password="AscZdvEfb520.+SQL"
            )

            mycursor = mydb.cursor()

            sql = "SELECT utilisateur, date_heure, contenu FROM serveurs WHERE date_heure > %s ORDER BY date_heure ASC"
            mycursor.execute(sql, (self.last_update,))

            serveurs = mycursor.fetchall()

            if serveurs:
                self.last_update = serveurs[-1][1]

            return serveurs

        except mysql.connector.Error as err:
            print("Une erreur MySQL s'est produite :", err)
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

    def open_chat(self):
        self.root.destroy()
        os.system('python3 tchat.py')

if __name__ == "__main__":
    app = ServeurP()

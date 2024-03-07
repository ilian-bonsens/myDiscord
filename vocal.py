import tkinter as tk
from tkinter import messagebox, PhotoImage, Toplevel
from PIL import Image, ImageTk  # Importer PIL pour gérer les images
import pyaudio
import wave
import base64
import mysql.connector
import io
from datetime import datetime
from connexion import Connexion

class Vocal(Connexion):
    def __init__(self, root=None):
        # Si aucun root n'est fourni, créer une nouvelle fenêtre Toplevel
        if root is None:
            self.root = Toplevel()
            self.root.title("Enregistreur Vocal")
        else:
            self.root = root

        # Configuration spécifique à Vocal
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.frames = []

        # Initialiser la base de données et l'interface utilisateur
        self.init_db()
        self.set_background()
        self.create_ui()
        
        super().__init__()

    def init_db(self):
        self.conn = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='AscZdvEfb520.+SQL', 
            database='Discord'  
        )
        self.cursor = self.conn.cursor()

    def start_recording(self):
        self.frames = []
        self.stream = self.p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
        self.stream.start_stream()
        print("Recording...")

    def stop_recording(self):
        print("Stopped recording.")
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        
        # Convertir les frames en base64
        buffer = io.BytesIO()
        wf = wave.open(buffer, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        audio_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Stocker dans la base de données
        self.save_to_db(audio_base64)

    def record_callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def save_to_db(self, audio_base64):
        now = datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
        utilisateur = self.prenom  # Utilisation de self.prenom hérité de Connexion
        try:
            # Modification de la requête pour inclure l'utilisateur
            query = "INSERT INTO messages (utilisateur, audio, date_heure) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (utilisateur, audio_base64, formatted_now))
            self.conn.commit()
            print("Vocal enregistré dans la base de données.")
        except mysql.connector.Error as e:
            print(e)
            print("Erreur lors de la sauvegarde de l'enregistrement.")

    def create_ui(self):
        # Charger et redimensionner les icônes des boutons
        play_icon = Image.open("images/play.png").resize((60, 60), Image.Resampling.LANCZOS)
        play_photo = ImageTk.PhotoImage(play_icon)
        stop_icon = Image.open("images/stop.png").resize((60, 60), Image.Resampling.LANCZOS)
        stop_photo = ImageTk.PhotoImage(stop_icon)

        # Calculer le positionnement pour centrer les boutons
        window_width, button_width, space_between_buttons = 450, 60, 60
        total_buttons_width = (button_width * 2) + space_between_buttons
        play_button_x = (window_width / 2) - (total_buttons_width / 2)
        stop_button_x = play_button_x + button_width + space_between_buttons
        buttons_y = 250 - 130

        # Dessiner un rectangle derrière les boutons
        rectangle_margin = 10
        self.canvas.create_rectangle(play_button_x - rectangle_margin, buttons_y - rectangle_margin, stop_button_x + button_width + rectangle_margin, buttons_y + button_width + rectangle_margin, fill="#2d243f", outline="")

        # Placer les boutons sur le Canvas
        play_button = tk.Button(self.canvas, image=play_photo, command=self.start_recording, borderwidth=0, highlightthickness=0, bg="#2d243f")
        play_button.image = play_photo
        play_button.place(x=play_button_x, y=buttons_y, width=60, height=60)
        stop_button = tk.Button(self.canvas, image=stop_photo, command=self.stop_recording, borderwidth=0, highlightthickness=0, bg="#2d243f")
        stop_button.image = stop_photo
        stop_button.place(x=stop_button_x, y=buttons_y, width=60, height=60)

    def set_background(self):
        self.root.geometry("450x250")  # Définir les dimensions de la fenêtre
        background_image = Image.open("images/vocal.png").resize((450, 250), Image.Resampling.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)
        self.canvas = tk.Canvas(self.root, width=450, height=250)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=background_photo, anchor="nw")
        self.canvas.background_photo = background_photo  # Garder une référence


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enregistreur Vocal")
    app = Vocal(root)
    root.mainloop()

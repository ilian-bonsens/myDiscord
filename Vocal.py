import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk  # Importer PIL pour gérer les images
import pyaudio
import wave
import base64
import mysql.connector
import io
from datetime import datetime

class Vocal:
    def __init__(self, root):
        self.root = root
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.frames = []
        
        self.init_db()
        self.set_background()  # Assurez-vous que set_background est appelé en premier
        self.create_ui()  # create_ui est appelé après que le canvas a été créé

    def init_db(self):
        self.conn = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='mars1993', 
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
        try:
            query = "INSERT INTO messages (audio, date_heure) VALUES (%s, %s)"
            self.cursor.execute(query, (audio_base64, formatted_now))
            self.conn.commit()
            # Affiche un message dans le terminal au lieu d'utiliser une messagebox
            print("Vocal enregistré dans la base de données.")
            self.root.destroy() # Ferme la fenêtre après l'enregistrement
        except mysql.connector.Error as e:
            print(e)
            # Vous pouvez également utiliser print pour signaler des erreurs
            print("Erreur lors de la sauvegarde de l'enregistrement.")

    def create_ui(self):
        # Charger et redimensionner l'icône du bouton de démarrage
        play_icon = Image.open("images/play.png")
        play_icon = play_icon.resize((60, 60), Image.Resampling.LANCZOS)  # Redimensionner à 20px de haut
        play_photo = ImageTk.PhotoImage(play_icon)
    
        # Charger et redimensionner l'icône du bouton d'arrêt
        stop_icon = Image.open("images/stop.png")
        stop_icon = stop_icon.resize((60, 60), Image.Resampling.LANCZOS)  # Redimensionner à 20px de haut
        stop_photo = ImageTk.PhotoImage(stop_icon)
        
        # Calculer le positionnement pour centrer les boutons
        window_width = 450  # La largeur de la fenêtre définie dans set_background
        button_width = 60  # La largeur des boutons
        space_between_buttons = 60  # L'espace entre les boutons
    
        # Total de l'espace occupé par les deux boutons et l'espace entre eux
        total_buttons_width = (button_width * 2) + space_between_buttons

        # Position X pour le premier bouton (play)
        play_button_x = (window_width / 2) - (total_buttons_width / 2)
        # Position X pour le second bouton (stop), qui est juste à côté du bouton play avec l'espace spécifié
        stop_button_x = play_button_x + button_width + space_between_buttons

        # Position Y pour les boutons, ajustée par rapport au bas de la fenêtre
        buttons_y = 250 - 130  # 250 est la hauteur de la fenêtre, ajustement de 100 pixels vers le haut

        # Dessiner un rectangle derrière les boutons
        rectangle_margin = 10  # Espace supplémentaire autour des boutons
        rect_x1 = play_button_x - rectangle_margin
        rect_y1 = buttons_y - rectangle_margin
        rect_x2 = stop_button_x + button_width + rectangle_margin
        rect_y2 = buttons_y + button_width + rectangle_margin

        # Création du rectangle sur le canvas avec le code couleur spécifié et sans contour
        self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="#2d243f", outline="")

        # Placer les boutons sur le Canvas
        play_button = tk.Button(self.canvas, image=play_photo, command=self.start_recording, borderwidth=0, highlightthickness=0, bg="#2d243f")
        play_button.image = play_photo  # Gardez une référence
        play_button.place(x=play_button_x, y=buttons_y, width=60, height=60)
    
        stop_button = tk.Button(self.canvas, image=stop_photo, command=self.stop_recording, borderwidth=0, highlightthickness=0, bg="#2d243f")
        stop_button.image = stop_photo  # Gardez une référence
        stop_button.place(x=stop_button_x, y=buttons_y, width=60, height=60)
        
    def set_background(self):
        # Définir les dimensions de la fenêtre
        self.root.geometry("450x250")  # Largeur x Hauteur

        # Charger et adapter l'image de fond
        background_image = Image.open("images/vocal.png")
        background_image = background_image.resize((450, 250), Image.Resampling.LANCZOS)  # Adapter l'image à la taille de la fenêtre
        background_photo = ImageTk.PhotoImage(background_image)

        # Créer un Canvas pour l'image de fond et les boutons
        self.canvas = tk.Canvas(self.root, width=450, height=250)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=background_photo, anchor="nw")
        self.canvas.background_photo = background_photo  # Garder une référence

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enregistreur Vocal")
    app = Vocal(root)
    root.mainloop()

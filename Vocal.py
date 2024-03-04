import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk  # Importer PIL pour gérer les images
import pyaudio
import wave
import base64
import mysql.connector
import io
from datetime import datetime
from connexion import Connexion

class Vocal(Connexion):
    def __init__(self, master=None):
        # Call the constructor of Connexion
        # It is assumed Connexion does not create a new window if master is provided.
        super().__init__(master)

        # Create a Toplevel window if Vocal is not provided with master
        if master is None:
            self.vocal_window = Toplevel()
            self.vocal_window.title("Enregistreur Vocal")
        else:
            self.vocal_window = master

        self.vocal_window.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close

        self.stream = None
        self.p = pyaudio.PyAudio()
        self.frames = []

        self.init_db()
        self.set_background()
        self.create_ui()

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
    # Calculer le positionnement pour centrer les boutons
    window_width, button_width, space_between_buttons = 450, 60, 60
    total_buttons_width = (button_width * 2) + space_between_buttons
    play_button_x = (window_width / 2) - (total_buttons_width / 2)
    stop_button_x = play_button_x + button_width + space_between_buttons
    buttons_y = 250 - 130

    # Dessiner un rectangle derrière les boutons
    rectangle_margin = 10
    self.canvas = tk.Canvas(self.vocal_window, width=450, height=250)
    self.canvas.pack(fill="both", expand=True)
    self.canvas.create_rectangle(
        play_button_x - rectangle_margin,
        buttons_y - rectangle_margin,
        stop_button_x + button_width + rectangle_margin,
        buttons_y + button_width + rectangle_margin,
        fill="#2d243f",
        outline=""
    )

    # Charger et redimensionner les icônes des boutons
    play_icon = Image.open("images/play.png").resize((60, 60), Image.Resampling.LANCZOS)
    play_photo = ImageTk.PhotoImage(play_icon)
    self.play_button = tk.Button(
        self.canvas,
        image=play_photo,
        command=self.start_recording,
        borderwidth=0,
        highlightthickness=0,
        bg="#2d243f"
    )
    self.play_button.image = play_photo  # Gardez une référence
    self.play_button.place(x=play_button_x, y=buttons_y, width=60, height=60)

    stop_icon = Image.open("images/stop.png").resize((60, 60), Image.Resampling.LANCZOS)
    stop_photo = ImageTk.PhotoImage(stop_icon)
    self.stop_button = tk.Button(
        self.canvas,
        image=stop_photo,
        command=self.stop_recording,
        borderwidth=0,
        highlightthickness=0,
        bg="#2d243f"
    )
    self.stop_button.image = stop_photo  # Gardez une référence
    self.stop_button.place(x=stop_button_x, y=buttons_y, width=60, height=60)


    def set_background(self):
        # Définir les dimensions de la fenêtre
        self.vocal_window.geometry("450x250")
        
        # Charger et adapter l'image de fond
        background_image = Image.open("images/vocal.png")
        background_image = background_image.resize((450, 250), Image.Resampling.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)

        # Créer un Canvas pour l'image de fond et les boutons
        self.canvas = tk.Canvas(self.vocal_window, width=450, height=250)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=background_photo, anchor="nw")
        self.canvas.background_photo = background_photo  # Garder une référence

    # ... Reste des méthodes de Vocal, si elles existent.

# Vérification pour exécuter Vocal comme script principal
if __name__ == "__main__":
    # Création de la fenêtre racine Tk si le script est exécuté directement
    root = tk.Tk()
    root.withdraw()  # La fenêtre principale est masquée, seul Vocal sera visible
    app = Vocal()  # Pas besoin de passer root ici, Vocal crée son propre Toplevel
    root.mainloop()






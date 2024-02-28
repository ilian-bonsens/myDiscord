import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
import base64
import mysql.connector
import io
from datetime import datetime

class AudioRecorder:
    def __init__(self, root):
        self.root = root
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.frames = []
        
        self.init_db()
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
        try:
            query = "INSERT INTO messages (audio, date_heure) VALUES (%s, %s)"
            self.cursor.execute(query, (audio_base64, formatted_now))
            self.conn.commit()
            messagebox.showinfo("Succès", "Enregistrement sauvegardé avec succès.")
        except mysql.connector.Error as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la sauvegarde de l'enregistrement.")

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        start_btn = tk.Button(frame, text="Démarrer l'enregistrement", command=self.start_recording)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(frame, text="Arrêter l'enregistrement", command=self.stop_recording)
        stop_btn.pack(side=tk.RIGHT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enregistreur Audio")
    app = AudioRecorder(root)
    root.mainloop()

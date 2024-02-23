import pyaudio
import wave
import mysql.connector
import os

# Configuration de la connexion à la base de données MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Remplacez par votre nom d'utilisateur MySQL
    'password': 'mars1993',  # Remplacez par votre mot de passe MySQL
    'database': 'Discord'  # Assurez-vous que cette base de données existe déjà dans MySQL
}

# Fonction pour enregistrer l'audio
def record_audio(record_seconds=5, output_filename="output.wav"):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Fonction pour sauvegarder l'audio dans la base de données MySQL, adaptée pour la table `messages`
def save_audio_to_db(db_config, audio_file_path):
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor()

    # Création de la table `messages` si elle n'existe pas
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INT AUTO_INCREMENT PRIMARY KEY, audio LONGBLOB NOT NULL)''')

    with open(audio_file_path, 'rb') as f:
        audio = f.read()

    c.execute("INSERT INTO messages (audio) VALUES (%s)", (audio,))

    conn.commit()
    conn.close()

# Main - enregistrement puis sauvegarde dans la DB
if __name__ == "__main__":
    audio_filename = "test.wav"
    
    # Enregistrez pendant combien de secondes vous voulez
    record_seconds = 10
    print(f"Recording for {record_seconds} seconds.")
    
    record_audio(record_seconds, audio_filename)
    save_audio_to_db(db_config, audio_filename)
    print(f"Audio file {audio_filename} has been saved to MySQL database in table `messages`.")

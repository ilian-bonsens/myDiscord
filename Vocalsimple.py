import mysql.connector
from datetime import datetime
import sounddevice as sd
import wavio

# Configuration de la base de données
db_config = {
    'user': 'root',
    'password': 'mars1993',
    'host': 'localhost',
    'database': 'Discord',
    'raise_on_warnings': True,
    'use_pure': True,  # Utilisez le pilote Python pur plutôt que le pilote C
    'autocommit': True,
    'charset': 'utf8mb4',  # Définissez explicitement le charset
    'collation': 'utf8mb4_general_ci',
}

# Fonction pour sauvegarder l'audio dans la base de données
def save_audio_to_db(config, audio_file_path):
    # Connectez-vous à la base de données
    cnx = mysql.connector.connect(**config)
    c = cnx.cursor()

    # Ouvrez le fichier audio en mode binaire
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Obtenez l'heure actuelle
    now = datetime.now()

    # Insérez les données audio et la date/heure dans la base de données
    try:
        c.execute("INSERT INTO messages (audio, date_heure) VALUES (%s, %s)", (audio_data, now))
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        c.close()
        cnx.close()

# Paramètres d'enregistrement
fs = 44100  # Fréquence d'échantillonnage
duration = 10  # Durée en secondes

# Enregistrement de l'audio
print("Recording for 10 seconds.")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
print("Recording finished.")

# Sauvegardez l'enregistrement dans un fichier WAV
audio_filename = 'output.wav'
wavio.write(audio_filename, myrecording, fs, sampwidth=2)

# Sauvegardez l'audio dans la base de données
save_audio_to_db(db_config, audio_filename)

print("Audio saved to database.")

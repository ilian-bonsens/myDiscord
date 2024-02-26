import mysql.connector
from datetime import datetime
import sounddevice as sd
import wavio
import gzip
import traceback

# Configuration de la base de données
db_config = {
    'user': 'root',
    'password': 'mars1993',
    'host': 'localhost',
    'database': 'Discord',
    'raise_on_warnings': True,
    'use_pure': True,
    'autocommit': True,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
}

# Fonction pour compresser l'audio
def compress_audio(audio_data):
    return gzip.compress(audio_data)

# Fonction pour sauvegarder l'audio compressé dans la base de données
def save_compressed_audio_to_db(config, audio_data):
    # Connectez-vous à la base de données
    cnx = mysql.connector.connect(**config)
    c = cnx.cursor()

    # Comprimez les données audio
    compressed_audio_data = compress_audio(audio_data)

    # Obtenez l'heure actuelle
    now = datetime.now()

    # Insérez l'audio compressé et la date/heure dans la base de données
    try:
        c.execute("INSERT INTO messages (audio, date_heure) VALUES (%s, %s)", (compressed_audio_data, now))
        cnx.commit()  # Commit explicitement, au cas où l'autocommit ne fonctionnerait pas
    except Exception as err:
        print(f"Something went wrong: {err}")
        traceback.print_exc()  # Cela affichera la trace complète de l'erreur
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

# Ouvrez le fichier audio en mode binaire et lisez-le
with open(audio_filename, 'rb') as audio_file:
    audio_data = audio_file.read()

# Sauvegardez l'audio compressé dans la base de données
save_compressed_audio_to_db(db_config, audio_data)

print("Compressed audio saved to database.")

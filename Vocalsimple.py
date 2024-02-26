import mysql.connector
from mysql.connector import Binary
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

# Fonction pour générer un nom unique pour l'audio
def generate_audio_title(c):
    c.execute("SELECT COUNT(*) FROM messages")
    count = c.fetchone()[0]
    return f"vocal{count+1}"

# Fonction pour sauvegarder l'audio compressé dans la base de données avec utilisateur
def save_compressed_audio_to_db(config, audio_data, user_id):
    # Connectez-vous à la base de données
    cnx = mysql.connector.connect(**config)
    c = cnx.cursor()

    # Générez un titre unique pour l'audio
    audio_title = generate_audio_title(c)

    # Comprimez les données audio
    compressed_audio_data = compress_audio(audio_data)

    # Obtenez l'heure actuelle
    now = datetime.now()

    # Insérez l'audio compressé, la date/heure et l'utilisateur dans la base de données
    try:
        query = "INSERT INTO messages (audio, date_heure, utilisateur) VALUES (%s, %s, %s)"
        c.execute(query, (compressed_audio_data, now, user_id))
        cnx.commit()  # N'oubliez pas de commit après l'insertion
        print(f"Compressed audio '{audio_title}' saved to database for user {user_id}.")
    except Exception as err:
        print(f"Something went wrong: {err}")
    finally:
        c.close()
        cnx.close()

# Paramètres d'enregistrement
fs = 44100  # Fréquence d'échantillonnage
duration = 5  # Durée en secondes

# Enregistrement de l'audio
print("Recording for 5 seconds.")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
print("Recording finished.")

# Sauvegardez l'enregistrement dans un fichier WAV
audio_filename = 'output.wav'
wavio.write(audio_filename, myrecording, fs, sampwidth=2)

# Ouvrez le fichier audio en mode binaire et lisez-le
with open(audio_filename, 'rb') as audio_file:
    audio_data = audio_file.read()

# Identifiant de l'utilisateur (doit être récupéré ou défini selon votre logique d'application)
user_id = "username123"

# Sauvegardez l'audio compressé dans la base de données
save_compressed_audio_to_db(db_config, audio_data, user_id)

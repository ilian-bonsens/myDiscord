import socket
import pyaudio
import sys

# Configuration de PyAudio
CHUNK = 1024  # Nombre d'échantillons audio par buffer
FORMAT = pyaudio.paInt16  # Format des échantillons audio
CHANNELS = 1  # Mono
RATE = 44100  # Fréquence d'échantillonnage

# Création d'une instance PyAudio
p = pyaudio.PyAudio()

# Ouverture du flux d'entrée (microphone)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Création d'un socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    client_socket.connect(('localhost', 12345))  # Assurez-vous que cette adresse et ce port correspondent à ceux du serveur

    print("Connexion au serveur réussie. Envoi de l'audio...")

    # Capture et envoi de l'audio en continu
    while True:
        data = stream.read(CHUNK)
        client_socket.sendall(data)

except KeyboardInterrupt:
    print("Arrêt manuel.")

except Exception as e:
    print(f"Erreur: {e}")

finally:
    # Fermeture du flux et du socket
    stream.stop_stream()
    stream.close()
    p.terminate()
    client_socket.close()
    print("Connexion fermée.")

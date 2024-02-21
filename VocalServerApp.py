import tkinter as tk
import socket
import threading
import pyaudio

class VoiceServerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Serveur d'Appel Vocal")

        # Configuration de l'interface
        self.status_label = tk.Label(self.master, text="En attente de connexion...")
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Démarrer le Serveur", command=self.start_server)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.master, text="Arrêter le Serveur", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Configuration du serveur
        self.server_socket = None
        self.client_connection = None
        self.server_running = False

        # Configuration audio
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None

    def start_server(self):
        self.server_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Serveur démarré. En attente de connexion...")

        threading.Thread(target=self.server_thread, daemon=True).start()

    def stop_server(self):
        self.server_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Serveur arrêté.")

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.client_connection:
            self.client_connection.close()

        if self.server_socket:
            self.server_socket.close()

        self.pyaudio_instance.terminate()

    def server_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('localhost', 12345))
            self.server_socket.listen(1)

            self.client_connection, addr = self.server_socket.accept()
            self.status_label.config(text=f"Connecté à {addr}")

            # Configuration du flux PyAudio pour la lecture
            self.stream = self.pyaudio_instance.open(format=pyaudio.paInt16,
                                                     channels=1,
                                                     rate=44100,
                                                     output=True)

            while self.server_running:
                data = self.client_connection.recv(1024)
                if not data:
                    break
                # Lecture des données audio reçues
                self.stream.write(data)

            self.client_connection.close()
            self.status_label.config(text="Connexion fermée.")
        except Exception as e:
            self.status_label.config(text=f"Erreur du serveur: {e}")
        finally:
            self.stop_server()

def main():
    root = tk.Tk()
    app = VoiceServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

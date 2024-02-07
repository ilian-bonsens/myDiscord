import customtkinter as ctk

class Fenetre:
    def __init__(self):
        self.app = ctk.CTk()
        self.framerate = 60
        self.app.title("Discord IML")
        self.app.geometry("1280x720")
        self.app.iconbitmap('images/discord-icon.ico')

    def mainloop(self):
        self.app.mainloop()

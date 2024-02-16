import flet as ft

class Message():  # Définit une classe Message avec un utilisateur, un texte et un type de message
    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type

def main(page: ft.Page):  # Définit la fonction principale qui prend une page comme argument

    chat = ft.Column()  # Crée une colonne pour le chat
    new_message = ft.TextField()  # Crée un champ de texte pour les nouveaux messages

    def on_message(message: Message):  # Définit une fonction qui sera exécutée lorsqu'un message est reçu
        if message.message_type == "chat_message":  # Si le message est un message de chat
            chat.controls.append(ft.Text(f"{message.user}: {message.text}"))  # Ajoute le message au chat
        elif message.message_type == "login_message":  # Si le message est un message de connexion
            chat.controls.append(  # Ajoute un message de connexion au chat
                ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            )
        page.update()

    page.pubsub.subscribe(on_message)  # S'abonne à la fonction on_message

    def send_click(e):  # Définit une fonction qui sera exécutée lorsqu'on clique sur le bouton "Send"
        page.pubsub.send_all(Message(user=page.session.get('user_name'), text=new_message.value, message_type="chat_message"))  # Envoie un message à tous les utilisateurs
        new_message.value = ""
        page.update()

    user_name = ft.TextField(label="Enter your name")  # Crée un champ de texte pour le nom de l'utilisateur

    def join_click(e):  # Définit une fonction qui sera exécutée lorsqu'on clique sur le bouton "Join chat"
        if not user_name.value:  # Si le champ de texte est vide
            user_name.error_text = "Name cannot be blank!"  # Affiche un message d'erreur
            user_name.update()  # Met à jour le champ de texte
        else:  # Si le champ de texte n'est pas vide
            page.session.set("user_name", user_name.value)  # Enregistre le nom de l'utilisateur
            page.dialog.open = False  # Ferme la boîte de dialogue
            page.pubsub.send_all(Message(user=user_name.value, text=f"{user_name.value} has joined the chat.", message_type="login_message"))  # Envoie un message de connexion à tous les utilisateurs
            page.update()

    # Crée une boîte de dialogue de bienvenue avec un champ de texte pour le nom de l'utilisateur et un bouton "Join chat"
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_click)],
        actions_alignment="end",
    )

    # Ajoute la colonne du chat et une ligne contenant le champ de texte et le bouton "Send" à la page
    page.add(chat, ft.Row([new_message, ft.ElevatedButton("Send", on_click=send_click)]))

ft.app(target=main, view=ft.WEB_BROWSER)  # Exécute l'application dans un navigateur web
import questionary
from controllers.auth import login_user

def main():
    print("\n EPIC EVENTS CRM \n")

    while True:
        choix = questionary.select(
            "Que voulez-vous faire ?",
            choices=[
                "Se connecter",
                "Quitter"
            ]
        ).ask()

        if choix == "Se connecter":
            username = questionary.text("Nom d'utilisateur :").ask()
            password = questionary.password("Mot de passe :").ask()

            token = login_user(username, password)

            if token:
                print("\n Vous êtes connecté.")
            else:
                print("\n Identifiants incorrects.")

        elif choix == "Quitter":
            print("Au revoir ")
            break

if __name__ == "__main__":
    main()
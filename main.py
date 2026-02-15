import questionary
import os
from controllers.auth import login_user, get_logged_user, TOKEN_FILE
from views.menus import menu_gestion_utilisateurs

def main():
    print("\n EPIC EVENTS CRM  \n")

    while True:
        # On vérifie si un User est déja connecté
        user = get_logged_user()

        if user:
            print(f"\n Connecté : {user['username']} - Rôle : {user['role']}")

            # On vérifie son role pour personnaliser le menu
            if user['role'] == "Gestion":
                choix = questionary.select(
                    "Menu Principal :",
                    choices=["Gérer les Collaborateurs", "Se déconnecter", "Quitter"]
                ).ask()
            else:
                choix = questionary.select(
                    "Menu Principal :",
                    choices=["Se déconnecter", "Quitter"]
                ).ask()

            # Menu des gestiionnaires
            if choix == "Gérer les Collaborateurs":
                menu_gestion_utilisateurs()

            # Autre options
            elif choix == "Se déconnecter":
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                print("Au revoir !")

            elif choix == "Quitter":
                print("Fermeture du programme.")
                break

        # Cas ou personne est connecté
        else:
            choix = questionary.select(
                "Accueil :",
                choices=["Se connecter", "Quitter"]
            ).ask()

            if choix == "Se connecter":
                identifiant = questionary.text("Identifiant :").ask()
                mot_de_passe = questionary.password("Mot de passe :").ask()

                token = login_user(identifiant, mot_de_passe)

                if token:
                    print(" Connexion réussie !")
                else:
                    print(" Erreur : Identifiant ou mot de passe incorrect.")

            elif choix == "Quitter":
                break

if __name__ == "__main__":
    main()
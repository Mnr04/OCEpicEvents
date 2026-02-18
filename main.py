import questionary
import os
from controllers.auth import login_user, get_logged_user, TOKEN_FILE
from views.menus import menu_gestion_utilisateurs, menu_gestion_clients, menu_gestion_contrats

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
                    choices=["Gérer les Collaborateurs", "Gérer les Contrats", "Se déconnecter", "Quitter"]
                ).ask()

            elif user['role'] == "Commercial":
                choix = questionary.select(
                    "Menu Principal :",
                    choices=["Gérer les Clients","Gérer les Contrats", "Se déconnecter", "Quitter"]
                ).ask()

            else:
                choix = questionary.select(
                    "Menu Principal :",
                    choices=["Se déconnecter", "Quitter"]
                ).ask()

            # Sous Menu Gestion
            if choix == "Gérer les Collaborateurs":
                menu_gestion_utilisateurs()

            if choix == "Gérer les Clients":
                menu_gestion_clients(user['user_id'])

            elif choix == "Gérer les Contrats":
                menu_gestion_contrats(user['role'], user['user_id'])

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
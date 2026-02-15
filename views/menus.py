import questionary
from controllers.users import create_user, get_all_users, update_user, delete_user

def menu_gestion_utilisateurs():
    while True:
        choix_menu = ["Créer un utilisateur", "Voir la liste", "Modifier un rôle", "Supprimer", "Retour"]

        action = questionary.select(
            "GESTION DES COLLABORATEURS :",
            choices=choix_menu
        ).ask()

        # Création d'un user
        if action == "Créer un utilisateur":
            print("\n--- Nouveau Collaborateur ---")
            nom = questionary.text("Nom de l'utilisateur :").ask()
            email = questionary.text("Email :").ask()
            mot_de_passe = questionary.password("Mot de passe :").ask()

            liste_roles = ["Gestion", "Commercial", "Support"]
            role_choisi = questionary.select("Choisissez un rôle :", choices=liste_roles).ask()

            creation_user = create_user(nom, email, mot_de_passe, role_choisi)

            if creation_user:
                print(" Collaborateur créé avec succès !")
            else:
                print("Erreur.")

        # List all Users
        elif action == "Voir la liste":
            tous_les_users = get_all_users()

            print("\n--- LISTE DES COLLABORATEURS ---")
            for utilisateur in tous_les_users:
                print(f" {utilisateur.username} | Email: {utilisateur.email} | Rôle: {utilisateur.role.value}")
            print("--------------------------------\n")

        # Update
        elif action == "Modifier un rôle":
            nom = questionary.text("Nom de l'utilisateur à modifier :").ask()

            liste_roles = ["Gestion", "Commercial", "Support"]
            nouveau_role = questionary.select("Nouveau Rôle :", choices=liste_roles).ask()

            if update_user(nom, nouveau_role):
                print("Le rôle a été modifié.")
            else:
                print("Erreur : Utilisateur introuvable.")

        # DELETE
        elif action == "Supprimer":
            nom = questionary.text("Nom de l'utilisateur à supprimer :").ask()

            confirmation = questionary.confirm(f"Êtes-vous sûr de vouloir supprimer {nom} ?").ask()

            if confirmation:
                if delete_user(nom):
                    print(" Utilisateur supprimé.")
                else:
                    print(" Erreur : Utilisateur introuvable.")
            else:
                print("Annulation.")

        elif action == "Retour":
            break
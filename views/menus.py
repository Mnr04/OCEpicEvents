import questionary
from controllers.users import create_user, get_all_users, update_user, delete_user
from controllers.clients import create_client, get_all_clients, update_client
from views.user_view import display_all_users

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

            if tous_les_users:
                display_all_users(tous_les_users)
            else:
                print("Aucun collaborateur trouvé.")

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

def menu_gestion_clients(user_id):
    while True:
        choix = questionary.select(
            "GESTION CLIENTS :",
            choices=["Nouveau Client", "Voir les Clients", "Modifier Client", "Retour"]
        ).ask()

        # Creation d'un client
        if choix == "Nouveau Client":
            nom = questionary.text("Nom :").ask()
            email = questionary.text("Email :").ask()
            tel = questionary.text("Téléphone :").ask()
            entreprise = questionary.text("Nom de l'entreprise :").ask()

            if create_client(nom, email, tel, entreprise, user_id):
                print("Client créé")
            else:
                print("Erreur")

        # Get All clients
        elif choix == "Voir les Clients":
            clients = get_all_clients()
            print("\n--- LISTE DES CLIENTS ---")
            for client in clients:
                print(f"{client.company_name} | Contact: {client.full_name} | Commercial ID: {client.commercial_contact_id}")
            print("-------------------------\n")

        # Update clients
        elif choix == "Modifier Client":
            nom_cible = questionary.text("Nom du client à modifier :").ask()
            nouvelle_boite = questionary.text("Nouveau nom d'entreprise :").ask()

            if update_client(nom_cible, nouvelle_boite, user_id):
                print("Client modifié.")
            else:
                print("Échec modification")

        elif choix == "Retour":
            break
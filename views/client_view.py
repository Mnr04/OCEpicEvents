from tabulate import tabulate

def afficher_tableau_clients(clients):
    if not clients:
        print("\n Aucun client à afficher.\n")
        return

    tableau = []

    for client in clients:
        ligne = [
            client.id,
            client.full_name,
            client.email,
            client.company_name,
            f"Commercial n°{client.commercial_contact_id}"
        ]
        tableau.append(ligne)

    headers = ["ID", "Nom", "Email", "Entreprise", "Contact Commercial"]

    print("\n--- LISTE DES CLIENTS ---")
    print(tabulate(tableau, headers=headers, tablefmt="grid"))
    print("\n")
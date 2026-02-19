from tabulate import tabulate

def display_all_users(users):

    if not users:
        print("\n Aucun utilisateur à afficher.\n")
        return

    tableau = []

    for user in users:
        ligne = [user.id, user.username, user.email, user.role.value]
        tableau.append(ligne)

    headers = ["ID", "Nom", "Email", "Rôle"]

    print("\n")
    print(tabulate(tableau, headers=headers, tablefmt="grid"))
    print("\n")
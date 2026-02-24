import click
from tabulate import tabulate

def display_all_users(users):
    if not users:
        click.secho("\n Aucun utilisateur à afficher.\n", fg="yellow")
        return

    tableau = []
    for user in users:
        ligne = [user.id, user.username, user.email, user.role.value]
        tableau.append(ligne)

    headers = ["ID", "Nom", "Email", "Rôle"]
    click.echo("\n--- LISTE DES COLLABORATEURS ---")
    click.echo(tabulate(tableau, headers=headers, tablefmt="grid"))
    click.echo("\n")
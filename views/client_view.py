import click
from tabulate import tabulate


def afficher_tableau_clients(clients):
    if not clients:
        click.secho("\nAucun client à afficher.\n", fg="yellow")
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
    click.echo("\n--- LISTE DES CLIENTS ---")
    click.echo(tabulate(tableau, headers=headers, tablefmt="grid"))
    click.echo("\n")

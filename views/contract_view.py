import click
from tabulate import tabulate

def afficher_tableau_contrats(contrats):
    if not contrats:
        click.secho("\n Aucun contrat à afficher.\n", fg="yellow")
        return

    tableau = []
    for contrat in contrats:
        statut = " SIGNÉ" if contrat.status else " NON SIGNÉ"
        paiement = " PAYÉ" if contrat.remaining_amount == 0 else f"Reste: {contrat.remaining_amount}€"

        ligne = [contrat.id, f"Client n°{contrat.client_id}", f"{contrat.total_amount} €", paiement, statut]
        tableau.append(ligne)

    headers = ["ID", "Client", "Montant Total", "Paiement", "Statut"]
    click.echo("\n--- LISTE DES CONTRATS ---")
    click.echo(tabulate(tableau, headers=headers, tablefmt="grid"))
    click.echo("\n")
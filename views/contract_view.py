from tabulate import tabulate

def afficher_tableau_contrats(contrats):
    if not contrats:
        print("\n Aucun contrat à afficher.\n")
        return

    tableau = []
    for contrat in contrats:

        statut = "SIGNÉ" if contrat.status else " NON SIGNÉ"
        paiement = "PAYÉ" if contrat.remaining_amount == 0 else f"Reste: {contrat.remaining_amount}€"

        ligne = [
            contrat.id,
            f"Client n°{contrat.client_id}",
            f"{contrat.total_amount} €",
            paiement,
            statut
        ]
        tableau.append(ligne)

    headers = ["ID", "Client", "Montant Total", "Paiement", "Statut"]

    print("\n--- LISTE DES CONTRATS ---")
    print(tabulate(tableau, headers=headers, tablefmt="grid"))
    print("\n")
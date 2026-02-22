from tabulate import tabulate

def afficher_tableau_events(events):
    if not events:
        print("\n Aucun événement à afficher.\n")
        return

    tableau = []
    for event in events:
        support = f"Support n°{event.support_contact_id}" if event.support_contact_id else "NON ASSIGNÉ"

        ligne = [
            event.id,
            f"Contrat n°{event.contract_id}",
            event.event_date_start,
            event.event_date_end,
            event.location,
            event.attendees,
            support
        ]
        tableau.append(ligne)

    headers = ["ID", "Contrat", "Début", "Fin", "Lieu", "Participants", "Support"]

    print("\n--- LISTE DES ÉVÉNEMENTS ---")
    print(tabulate(tableau, headers=headers, tablefmt="grid"))
    print("\n")
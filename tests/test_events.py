from controllers.users import create_user, delete_user
from controllers.clients import create_client, delete_client
from controllers.contracts import create_contract, update_contract, delete_contract
from controllers.events import create_event, update_event, delete_event, get_all_events
from models.models import User, Client, Contract, Event
from database import Session
from datetime import datetime, timedelta

def test_crud_events():
    delete_client("Client_Event")
    delete_user("comercial_01")
    delete_user("support_01")

    create_user("comercial_01", "c01@event.com", "123", "Commercial")
    create_user("support_01", "s01@event.com", "123", "Support")

    session = Session()
    comm_id = session.query(User).filter_by(username="comercial_01").first().id
    supp_id = session.query(User).filter_by(username="support_01").first().id
    session.close()

    # commercial crée un client
    create_client("Client_Event", "c01@cli.com", "00", "Boite", comm_id)
    session = Session()
    client_id = session.query(Client).filter_by(full_name="Client_Event").first().id
    session.close()

    # La gestion crée un contrat
    create_contract(client_id, 1000.0, 1000.0, "Gestion")
    session = Session()
    contrat = session.query(Contract).filter_by(client_id=client_id).first()
    contrat_id = contrat.id
    session.close()

    date_debut = datetime.now()
    date_fin = date_debut + timedelta(days=2)

    # Le commercia créer l'événement --> Le contrat n'est pas signé. Return False
    result = create_event(contrat_id, date_debut, date_fin, "Paris", 50, "Test", "Commercial", comm_id)
    assert result is False

    # Le commercial signe le contrat
    update_contract(contrat_id, "Commercial", comm_id, nouveau_statut=True)

   # Le commercia créer l'événement --> Le contrat n'est pas signé. Return True
    result = create_event(contrat_id, date_debut, date_fin, "Paris", 50, "Test", "Commercial", comm_id)
    assert result is True

    # Récupération de l'événement
    session = Session()
    event = session.query(Event).filter_by(contract_id=contrat_id).first()
    event_id = event.id
    session.close()

    # La Gestion assigne le Support à l'événement
    update_event(event_id, "Gestion", 999, nouveau_support_id=supp_id)

    session = Session()
    event_assigne = session.query(Event).filter_by(id=event_id).first()
    assert event_assigne.support_contact_id == supp_id
    session.close()

    # Le Support met à jour l'événement
    update_event(event_id, "Support", supp_id, nouvelles_notes="Notes modifiées")

    session = Session()
    event_modifie = session.query(Event).filter_by(id=event_id).first()
    assert event_modifie.notes == "Notes modifiées"
    session.close()

    delete_event(event_id)
    delete_contract(contrat_id, "Gestion")
    delete_client("Client_Event")
    delete_user("comercial_01")
    delete_user("support_01")
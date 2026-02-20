from controllers.contracts import get_contracts_unsigned, get_contracts_unpaid
from controllers.users import create_user, delete_user
from controllers.clients import create_client, delete_client
from controllers.contracts import (
    create_contract, update_contract, delete_contract,
)
from models.models import User, Client, Contract
from database import Session

def test_contract_filters():
    delete_client("Client_01")
    delete_user("Commercial_01")

    # On crée un commercial et un client
    create_user("Commercial_01", "c01@test.com", "123", "Commercial")
    session = Session()
    comm_id = session.query(User).filter_by(username="Commercial_01").first().id
    session.close()

    create_client("Client_01", "c01@filtre.com", "000", "Societe_1", comm_id)
    session = Session()
    client_id = session.query(Client).filter_by(full_name="Client_01").first().id
    session.close()

    # On crée un contrat
    create_contract(client_id, 2000.0, 2000.0, "Gestion")
    session = Session()
    contrat = session.query(Contract).filter_by(client_id=client_id).first()
    contrat_id = contrat.id
    session.close()

    # Test contrat non payé
    non_payes = get_contracts_unpaid()
    ids_non_payes = [c.id for c in non_payes]
    assert contrat_id in ids_non_payes

    # B. Test contrat non signé
    non_signes = get_contracts_unsigned()
    ids_non_signes = [c.id for c in non_signes]
    assert contrat.id in ids_non_signes

    # On update le contrat en le signat
    update_contract(contrat_id, "Commercial", comm_id, nouveau_statut=True)

    non_signes_apres = get_contracts_unsigned()
    ids_non_signes_apres = [c.id for c in non_signes_apres]
    assert contrat_id not in ids_non_signes_apres

    # Clean code
    delete_contract(contrat_id, "Gestion")
    delete_client("Client_01")
    delete_user("Commercial_01")
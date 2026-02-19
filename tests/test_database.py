import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, UserRole, Client, Contract
from database import Session
from controllers.users import create_user, get_all_users, update_user, delete_user
from controllers.clients import create_client, get_all_clients, update_client
from controllers.contracts import create_contract, get_all_contracts, update_contract, delete_contract

def test_create_user():
    DB_FILE = "test_temporaire.db"

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    engine = create_engine(f"sqlite:///{DB_FILE}")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = User(
        username="test",
        email="test@email.com",
        password_hash="test123",
        role=UserRole.COMMERCIAL
    )
    session.add(new_user)
    session.commit()

    user_trouve = session.query(User).filter_by(username="test").first()
    assert user_trouve is not None

    session.close()
    os.remove(DB_FILE)


def test_crud_users():
    delete_user("test")

    # Create
    user = create_user("test", "test@epicevents.com", "password123", "Commercial")
    assert user is True

    # Get ALL
    tous_les_users = get_all_users()
    noms = [user.username for user in tous_les_users]
    assert "test" in noms

    # Update
    update_user("test", "Support")
    session = Session()
    user_modifie = session.query(User).filter_by(username="test").first()
    assert user_modifie.role.value == "Support"
    session.close()

    # DELETE
    delete_user("test")
    session = Session()
    user_supprime = session.query(User).filter_by(username="test").first()
    assert user_supprime is None
    session.close()


def test_crud_clients():
    delete_user("commercial_01")

    # Create commercial
    create_user("commercial_01", "commercial@test.com", "123", "Commercial")
    session = Session()
    commercial = session.query(User).filter_by(username="commercial_01").first()
    session.close()

    # Create Client
    resultat = create_client("Client_Test", "client@test.com", "123", "societe_01", commercial.id)
    assert resultat is True

    # Get All
    tous_les_clients = get_all_clients()
    noms = [client.full_name for client in tous_les_clients]
    assert "Client_Test" in noms

    #  UPDATE
    update = update_client("Client_Test", "Nouvelle Entreprise", commercial.id)
    assert update is True

    session = Session()
    client_modifie = session.query(Client).filter_by(full_name="Client_Test").first()
    assert client_modifie.company_name == "Nouvelle Entreprise"

    # Sécurity other commercial id dont update other client
    update = update_client("Client_Test", "society_02", 18)
    assert update is False
    session.close()

    # Delete client
    session = Session()
    client = session.query(Client).filter_by(full_name="Client_Test").first()
    if client:
        session.delete(client)
        session.commit()
    session.close()

    delete_user("commercial_01")


def test_crud_contracts():

    delete_user("commercial_01")
    # Création d'un commercial
    create_user("commercial_01", "commercial_01@test.com", "123", "Commercial")

    session = Session()
    commercial = session.query(User).filter_by(username="commercial_01").first()
    session.close()

    #Creation d'un client
    create_client("Client_Test", "client01@test.com", "0606060606", "Societe_01", commercial.id)

    session = Session()
    client = session.query(Client).filter_by(full_name="Client_Test").first()
    client_id = client.id
    session.close()

    # La gestion creer un contrat
    resultat = create_contract(client_id, 5000.0, 5000.0, "Gestion")
    assert resultat is True

    # Get contrat ID
    session = Session()
    contrat = session.query(Contract).filter_by(client_id=client_id).first()
    session.close()

    # GET ALL
    tous_les_contrats = get_all_contracts()
    all_ids = [contract.id for contract in tous_les_contrats]
    assert contrat.id in all_ids

    # UPDATE
    update_ok = update_contract(contrat.id, "Commercial", commercial.id, nouveau_statut=True)
    assert update_ok is True

    # Vérif contrat signé
    session = Session()
    contrat_verif = session.query(Contract).filter_by(id=contrat.id).first()
    assert contrat_verif.status is True
    session.close()

    # On verifie si un commercial peut modifier un autre contrat
    update = update_contract(contrat.id, "Commercial", 666, nouveau_statut=False)
    assert update is False

    # DELETE (Only Gestion)
    delete = delete_contract(contrat.id, "Gestion")
    assert delete is True

    # Verif contrat delete
    session = Session()
    contrat_to_delete = session.query(Contract).filter_by(id=contrat.id).first()
    assert contrat_to_delete is None
    session.close()

    # Delete client
    session = Session()
    client = session.query(Client).filter_by(full_name="Client_Test").first()
    if client:
        session.delete(client)
        session.commit()
    session.close()

    delete_user("commercial_01")
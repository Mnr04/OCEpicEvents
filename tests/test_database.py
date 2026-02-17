import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, UserRole, Client
from database import Session
from controllers.users import create_user, get_all_users, update_user, delete_user
from controllers.clients import create_client, get_all_clients, update_client

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
    resultat = create_client("Client Test", "client@test.com", "123", "societe_01", commercial.id)
    assert resultat is True

    # Get All
    tous_les_clients = get_all_clients()
    noms = [client.full_name for client in tous_les_clients]
    assert "Client Test" in noms

    #  UPDATE
    update = update_client("Client Test", "Nouvelle Entreprise", commercial.id)
    assert update is True

    session = Session()
    client_modifie = session.query(Client).filter_by(full_name="Client Test").first()
    assert client_modifie.company_name == "Nouvelle Entreprise"

    # Sécurity other commercial id dont update other client
    update = update_client("Client Test", "society_02", 18)
    assert update is False
    session.close()

    delete_user("comm_test")
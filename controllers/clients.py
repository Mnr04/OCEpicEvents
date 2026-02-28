from models.models import Client
from database import Session
from sqlalchemy.exc import IntegrityError
import sentry_sdk


def create_client(nom, email, telephone, entreprise, commercial_id):
    """
    Create a new client and link them to a sales contact (commercial).
    Returns True on success, False on error.
    """
    session = Session()

    nouveau_client = Client(
        full_name=nom,
        email=email,
        phone=telephone,
        company_name=entreprise,
        commercial_contact_id=commercial_id
    )

    try:
        session.add(nouveau_client)
        session.commit()
        session.close()
        return True
    except IntegrityError as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        session.close()
        return False


def get_all_clients():
    """
    Return a list of all clients.
    """
    session = Session()
    clients = session.query(Client).all()
    session.close()
    return clients


def update_client(nom_client, nouvelle_entreprise, commercial_id_connecte):
    """
    Update the company name of a client.
    Checks if the connected user is the commercial contact for this client.
    """
    session = Session()
    client = session.query(Client).filter_by(full_name=nom_client).first()

    if client:
        if client.commercial_contact_id != commercial_id_connecte:
            session.close()
            return False

        client.company_name = nouvelle_entreprise
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False


def delete_client(client_name):
    """
    Delete a client by their full name.
    """
    session = Session()
    client = session.query(Client).filter_by(full_name=client_name).first()

    if client:
        session.delete(client)
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False

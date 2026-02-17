from models.models import Client, Session
from sqlalchemy.exc import IntegrityError

def create_client(nom, email, telephone, entreprise, commercial_id):
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
    except IntegrityError:
        session.rollback()
        session.close()
        return False

def get_all_clients():
    session = Session()
    clients = session.query(Client).all()
    session.close()
    return clients

def update_client(nom_client, nouvelle_entreprise, commercial_id_connecte):
    session = Session()
    client = session.query(Client).filter_by(full_name=nom_client).first()

    if client:
        if client.commercial_contact_id != commercial_id_connecte:
            print("Ce n'est pas votre client !")
            session.close()
            return False

        client.company_name = nouvelle_entreprise
        session.commit()
        session.close()
        return True

    session.close()
    return False
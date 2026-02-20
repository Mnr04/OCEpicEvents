from models.models import Contract, Client
from database import Session

def create_contract(client_id, montant_total, reste_a_payer, user_role):
    if user_role != "Gestion":
        print("ERREUR : Seule la Gestion peut créer un contrat.")
        return False

    session = Session()

    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        print("Client introuvable.")
        session.close()
        return False

    nouveau_contrat = Contract(
        client_id=client.id,
        commercial_contact_id=client.commercial_contact_id,
        total_amount=montant_total,
        remaining_amount=reste_a_payer,
        status=False
    )

    session.add(nouveau_contrat)
    session.commit()
    session.close()
    return True

def update_contract(contract_id, user_role, user_id, nouveau_statut=None, nouveau_montant=None):
    session = Session()
    contrat = session.query(Contract).filter_by(id=contract_id).first()

    if not contrat:
        print(" Contrat introuvable.")
        session.close()
        return False

    # ils peuvent Créer et modifier tous les contrats
    if user_role == "Gestion":
        if nouveau_montant:
            contrat.total_amount = nouveau_montant
        if nouveau_statut is not None:
            contrat.status = nouveau_statut

        session.commit()
        session.close()
        return True

    # seulement les contrats des clients dont ils sont responsables
    elif user_role == "Commercial":
        if contrat.commercial_contact_id != user_id:
            print("Ce contrat ne vous appartient pas !")
            session.close()
            return False

        if nouveau_statut is not None:
            contrat.status = nouveau_statut
            session.commit()
            session.close()
            return True
        else:
            print("Vous ne pouvez modifier que le statut.")
            session.close()
            return False

    session.close()
    return False

def get_all_contracts():
    session = Session()
    contrats = session.query(Contract).all()
    session.close()
    return contrats

def delete_contract(contract_id, user_role):
    if user_role != "Gestion":
        print("Action interdite Gestion only")
        return False

    session = Session()
    contrat = session.query(Contract).filter_by(id=contract_id).first()

    if contrat:
        session.delete(contrat)
        session.commit()
        session.close()
        return True

    print("Contrat introuvable.")
    session.close()
    return False

def get_contracts_unsigned():
    session = Session()
    contrats = session.query(Contract).filter_by(status=False).all()
    session.close()
    return contrats

def get_contracts_signed():
    session = Session()
    contrats = session.query(Contract).filter_by(status=True).all()
    session.close()
    return contrats

def get_contracts_unpaid():
    session = Session()
    contrats = session.query(Contract).filter(Contract.remaining_amount > 0).all()
    session.close()
    return contrats
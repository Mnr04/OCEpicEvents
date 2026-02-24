from models.models import Event, Contract
from database import Session

def create_event(contract_id, date_start, date_end, location, attendees, notes, user_role, user_id):
    if user_role != "Commercial":
        return False

    session = Session()
    contrat = session.query(Contract).filter_by(id=contract_id).first()

    if not contrat:
        session.close()
        return False

    # On vérifie que ce contrat appartient à nos clients
    if contrat.commercial_contact_id != user_id:
        session.close()
        return False

    # Verifie que le contrat est signé
    if contrat.status is False:
        session.close()
        return False

    # Create
    nouveau_event = Event(
        contract_id=contrat.id,
        event_date_start=date_start,
        event_date_end=date_end,
        location=location,
        attendees=attendees,
        notes=notes,
        support_contact_id=None
    )

    session.add(nouveau_event)
    session.commit()
    session.close()
    return True

def get_all_events():
    session = Session()
    events = session.query(Event).all()
    session.close()
    return events

def update_event(event_id, user_role, user_id, nouveau_support_id=None, nouvelles_notes=None):
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()

    if not event:
        session.close()
        return False

    if user_role == "Gestion":
        if nouveau_support_id is not None:
            event.support_contact_id = nouveau_support_id
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

    elif user_role == "Support":
        if event.support_contact_id != user_id:
            session.close()
            return False

        if nouvelles_notes is not None:
            event.notes = nouvelles_notes
            session.commit()
            session.close()
            return True

    session.close()
    return False

def delete_event(event_id):
    session = Session()
    event = session.query(Event).filter_by(id=event_id).first()
    if event:
        session.delete(event)
        session.commit()
        session.close()
        return True
    session.close()
    return False

def get_events_without_support():
    session = Session()
    events = session.query(Event).filter_by(support_contact_id=None).all()
    session.close()
    return events

def get_my_events(user_id):
    session = Session()
    events = session.query(Event).filter_by(support_contact_id=user_id).all()
    session.close()
    return events
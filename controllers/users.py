from models.models import User, UserRole
from database import Session
from sqlalchemy.exc import IntegrityError
import hashlib

ROLE_MAP = {
    "Gestion": UserRole.GESTION,
    "Support": UserRole.SUPPORT,
    "Commercial": UserRole.COMMERCIAL
}

def create_user(username, email, password, role_name):
    session = Session()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    role = ROLE_MAP.get(role_name)

    new_user = User(username=username, email=email, password_hash=password_hash, role = role)

    try:
        session.add(new_user)
        session.commit()
        session.close()
        return True
    except IntegrityError:
        session.rollback()
        session.close()
        return False

def get_all_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

def update_user(username, new_role):
    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if user and new_role in ROLE_MAP:
        user.role = ROLE_MAP[new_role]
        session.commit()
        session.close()
        return True

    session.close()
    return False

def delete_user(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if user:
        session.delete(user)
        session.commit()
        session.close()
        return True

    session.close()
    return False
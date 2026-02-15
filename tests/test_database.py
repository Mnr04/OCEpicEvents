import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, UserRole
from database import Session
from controllers.users import create_user, get_all_users, update_user, delete_user

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
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, UserRole

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


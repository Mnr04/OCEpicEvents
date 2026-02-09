from database import engine, Base, SessionLocal
from models import User, UserRole

def init_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = SessionLocal()

    admin_user = User(
        username="admin",
        email="admin@epicevents.com",
        password_hash="admin123",
        role=UserRole.GESTION
    )

    session.add(admin_user)
    session.commit()

    session.close()

if __name__ == "__main__":
    init_database()
from database import engine, Base, Session
from models.models import User, UserRole
from utils import hash_password

def init_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    admin_user = User(
        username="admin",
        email="admin@epicevents.com",
        password_hash= hash_password("admin123"),
        role=UserRole.GESTION
    )

    session.add(admin_user)
    session.commit()

    session.close()

if __name__ == "__main__":
    init_database()
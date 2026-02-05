import enum
from sqlalchemy import Column, Integer, String, Enum
from database import Base

class UserRole(enum.Enum):
    GESTION = "Gestion"
    COMMERCIAL = "Commercial"
    SUPPORT = "Support"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole), nullable=False)

    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"
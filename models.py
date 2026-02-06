import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
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


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=False)

    creation_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    commercial_contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)

import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Float, Boolean
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

    clients = relationship("Client", back_populates="commercial_contact")
    contracts = relationship("Contract", back_populates="commercial_contact")


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
    commercial_contact = relationship("User", back_populates="clients")

    contracts = relationship("Contract", back_populates="client")



class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    status = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship("Client", back_populates="contracts")

    commercial_contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    commercial_contact = relationship("User", back_populates="contracts")



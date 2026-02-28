import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class UserRole(enum.Enum):
    GESTION = "Gestion"
    COMMERCIAL = "Commercial"
    SUPPORT = "Support"


class User(Base):
    """
    Represents a company employee in the database.
    Employees can have one of three roles: Gestion, Commercial, or Support.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # All relations
    clients = relationship("Client", back_populates="commercial_contact")
    contracts = relationship("Contract", back_populates="commercial_contact")
    events = relationship("Event", back_populates="support_contact")


class Client(Base):
    """
    Represents a client company or individual.
    Each client is linked to a specific commercial contact.
    """
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Link to commercial
    commercial_contact_id = Column(
        Integer, ForeignKey('users.id'), nullable=False
        )
    commercial_contact = relationship("User", back_populates="clients")

    # relation to contract
    contracts = relationship(
        "Contract", back_populates="client", cascade="all, delete-orphan"
        )


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    status = Column(Boolean, default=False)

    # Link to client
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship("Client", back_populates="contracts")

    # Link to commercial
    commercial_contact_id = Column(
        Integer, ForeignKey('users.id'), nullable=False
        )
    commercial_contact = relationship("User", back_populates="contracts")

    # relation to event
    events = relationship(
        "Event", back_populates="contract", cascade="all, delete-orphan"
        )


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    attendees = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    # Link to contract
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    contract = relationship("Contract", back_populates="events")

    # Link to Support
    support_contact_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    support_contact = relationship("User", back_populates="events")

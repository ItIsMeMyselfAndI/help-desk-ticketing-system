from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    # for issuer only
    issued_tickets = relationship("Ticket", back_populates="issuer", foreign_keys='Ticket.issuer_id')
    # for assignee only
    assigned_tickets = relationship("Ticket", back_populates="assignee", foreign_keys='Ticket.assignee_id')
    # for sender only
    sent_messages = relationship("TicketMessage", back_populates="sender", foreign_keys='TicketMessage.sender_id')
    # for receiver only
    received_messages = relationship("TicketMessage", back_populates="receiver", foreign_keys='TicketMessage.receiver_id')


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    issuer_id = Column(Integer, ForeignKey('users.id'), index=True)
    assignee_id = Column(Integer, ForeignKey('users.id'), index=True)
    # relationships 
    issuer = relationship("User", back_populates="issued_tickets", foreign_keys=[issuer_id])
    assignee = relationship("User", back_populates="assigned_tickets", foreign_keys=[assignee_id])
    attachments = relationship("TicketAttachment", back_populates="ticket", foreign_keys="TicketAttachment.ticket_id")
    messages = relationship("TicketMessage", back_populates="ticket", foreign_keys="TicketMessage.ticket_id")


class TicketAttachment(Base):
    __tablename__ = "ticket_attachments"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    size = Column(Integer, index=True)
    filetype = Column(String, index=True)
    uploaded_at = Column(DateTime, index=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), index=True)
    # relationships 
    ticket = relationship("Ticket", back_populates="attachments", foreign_keys=[ticket_id])


class TicketMessage(Base):
    __tablename__ = "ticket_messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), index=True)
    receiver_id = Column(Integer, ForeignKey('users.id'), index=True)
    sent_at = Column(DateTime, index=True)
    # relationships 
    ticket = relationship("Ticket", back_populates="messages", foreign_keys=[ticket_id])
    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])



from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(index=True)
    updated_at: Mapped[datetime] = mapped_column(index=True)
    # for issuer only (all roles)
    issued_tickets: Mapped[List["Ticket"]] = relationship(back_populates="issuer", foreign_keys='Ticket.issuer_id')
    # for assignee only (support staff)
    assigned_tickets: Mapped[Optional[List["Ticket"]]] = relationship(back_populates="assignee", foreign_keys='Ticket.assignee_id')
    # for sender only (all roles)
    sent_messages: Mapped[List["TicketMessage"]] = relationship(back_populates="sender", foreign_keys='TicketMessage.sender_id')
    # for receiver only (all roles)
    received_messages: Mapped[List["TicketMessage"]] = relationship(back_populates="receiver", foreign_keys='TicketMessage.receiver_id')


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(index=True)
    category: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(index=True)
    updated_at: Mapped[datetime] = mapped_column(index=True)
    issuer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    assignee_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    # relationships 
    issuer: Mapped["User"] = relationship(back_populates="issued_tickets", foreign_keys=[issuer_id])
    assignee: Mapped[Optional["User"]] = relationship(back_populates="assigned_tickets", foreign_keys=[assignee_id])
    attachments: Mapped[List["TicketAttachment"]] = relationship(back_populates="ticket", foreign_keys="TicketAttachment.ticket_id")
    messages: Mapped[List["TicketMessage"]] = relationship(back_populates="ticket", foreign_keys="TicketMessage.ticket_id")


class TicketAttachment(Base):
    __tablename__ = "ticket_attachments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(index=True)
    size: Mapped[int] = mapped_column(index=True)
    filetype: Mapped[str] = mapped_column(index=True)
    uploaded_at: Mapped[datetime] = mapped_column(index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('tickets.id'), index=True)
    # relationships 
    ticket: Mapped["Ticket"] = relationship(back_populates="attachments", foreign_keys=[ticket_id])


class TicketMessage(Base):
    __tablename__ = "ticket_messages"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(index=True)
    sent_at: Mapped[datetime] = mapped_column(index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('tickets.id'), index=True)
    # relationships 
    sender: Mapped["User"] = relationship(back_populates="sent_messages", foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship(back_populates="received_messages", foreign_keys=[receiver_id])
    ticket: Mapped["Ticket"] = relationship(back_populates="messages", foreign_keys=[ticket_id])



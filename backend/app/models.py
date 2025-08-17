from .constants import TicketStatus, TicketCategory
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from datetime import datetime
from typing import Optional, List

# for shared metadata
class Base(DeclarativeBase):
    pass


# users
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # details
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    # dates
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # relationships
    issued_tickets: Mapped[List["Ticket"]] = relationship(back_populates="issuer", foreign_keys="Ticket.issuer_id")
    assignee_tickets: Mapped[List["Ticket"]] = relationship(back_populates="assignee", foreign_keys="Ticket.assignee_id")
    sent_messages: Mapped[List["Message"]] = relationship(back_populates="sender", foreign_keys="Message.sender_id")
    received_messages: Mapped[List["Message"]] = relationship(back_populates="receiver", foreign_keys="Message.receiver_id")


# tickets
class Ticket(Base):
    __tablename__ = "tickets"
    # ids
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    issuer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    # details
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    status: Mapped[TicketStatus] = mapped_column(String, default=TicketStatus.OPEN, nullable=False)
    category: Mapped[Optional[TicketCategory]] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    # dates
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # relationships
    issuer: Mapped[User] = relationship(back_populates="issued_tickets", foreign_keys=[issuer_id])
    assignee: Mapped[Optional[User]] = relationship(back_populates="assignee_tickets", foreign_keys=[assignee_id])
    attachments: Mapped[List["Attachment"]] = relationship(back_populates="ticket")
    messages: Mapped[List["Message"]] = relationship(back_populates="ticket")


# attachments
class Attachment(Base):
    __tablename__ = "attachments"
    # ids
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), index=True)
    # details
    filename: Mapped[str] = mapped_column(nullable=False)
    filetype: Mapped[str] = mapped_column(nullable=False)
    filesize: Mapped[int] = mapped_column(nullable=False)
    # date
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # relationships
    ticket: Mapped[Ticket] = relationship(back_populates="attachments")


# messages
class Message(Base):
    __tablename__ = "messages"
    # ids
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), index=True)
    # details
    content: Mapped[str] = mapped_column(nullable=False)
    # TODO: emojis
    # date
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    edited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # relationships
    sender: Mapped[User] = relationship(back_populates="sent_messages", foreign_keys=sender_id)
    receiver: Mapped[User] = relationship(back_populates="received_messages", foreign_keys=receiver_id)
    ticket: Mapped[Ticket] = relationship(back_populates="messages", foreign_keys=ticket_id)


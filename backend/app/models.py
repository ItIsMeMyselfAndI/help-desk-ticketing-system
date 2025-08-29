from sqlalchemy import DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from datetime import datetime
from typing import Dict, Optional, List, Union

from app.constants import UserRole, TicketStatus, TicketCategory

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
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    # dates
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # relationships
    issued_tickets: Mapped[List["Ticket"]] = relationship(back_populates="issuer", foreign_keys="Ticket.issuer_id", cascade="all, delete")
    assignee_tickets: Mapped[List["Ticket"]] = relationship(back_populates="assignee", foreign_keys="Ticket.assignee_id", cascade="all, delete")
    sent_messages: Mapped[List["Message"]] = relationship(back_populates="sender", foreign_keys="Message.sender_id", cascade="all, delete")
    received_messages: Mapped[List["Message"]] = relationship(back_populates="receiver", foreign_keys="Message.receiver_id", cascade="all, delete")
    # dict ver
    def as_dict(self) -> Dict:
        return {
                "id": self.id,
                "username": self.username,
                "email": self.email,
                "role": self.role,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }


# tickets
class Ticket(Base):
    __tablename__ = "tickets"
    # ids
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    issuer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, default=None, index=True)
    # details
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    category: Mapped[Optional[TicketCategory]] = mapped_column(Enum(TicketCategory), nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    # dates
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # relationships
    issuer: Mapped[User] = relationship(back_populates="issued_tickets", foreign_keys=[issuer_id])
    assignee: Mapped[Optional[User]] = relationship(back_populates="assignee_tickets", foreign_keys=[assignee_id])
    attachments: Mapped[List["Attachment"]] = relationship(back_populates="ticket", cascade="all, delete")
    messages: Mapped[List["Message"]] = relationship(back_populates="ticket", cascade="all, delete")
    # dict ver
    def as_dict(self) -> Dict:
        return {
                "id": self.id,
                "issuer_id": self.issuer_id,
                "assignee_id": self.assignee_id,
                "title": self.title,
                "status": self.status,
                "category": self.category,
                "description": self.description,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }


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
    # dict ver
    def as_dict(self) -> Dict:
        return {
                "id": self.id,
                "ticket_id": self.ticket_id,
                "filename": self.filename,
                "filetype": self.filetype,
                "filesize": self.filesize,
                "uploaded_at": self.uploaded_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }


# messages
class Message(Base):
    __tablename__ = "messages"
    # ids
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
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
    # dict ver
    def as_dict(self) -> Dict:
        return {
                "id": self.id,
                "ticket_id": self.ticket_id,
                "sender_id": self.sender_id,
                "receiver_id": self.receiver_id,
                "content": self.content,
                "sent_at": self.sent_at.isoformat(),
                "edited_at": self.edited_at.isoformat()
                }


# ----
TableModels = Union[User, Ticket, Attachment, Message]

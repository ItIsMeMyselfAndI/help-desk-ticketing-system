from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

from app.constants import UserRole, TicketStatus, TicketCategory


class ORMBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # for attr + dict access + model compatibility
    )


# users
class UserBase(ORMBase):
    username: str
    email: EmailStr
    role: UserRole
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(ORMBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class UserOut(UserBase):
    id: int


class UserRef(ORMBase):
    id: int
    username: str


# tickets
class TicketBase(ORMBase):
    title: str
    status: TicketStatus
    category: Optional[TicketCategory] = None
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TicketCreate(TicketBase):
    issuer_id: int
    assignee_id: Optional[int] = None


class TicketUpdate(ORMBase):
    issuer_id: Optional[int] = None
    assignee_id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[TicketStatus] = None
    category: Optional[TicketCategory] = None
    description: Optional[str] = None


class TicketOut(TicketBase):
    id: int
    issuer: UserRef
    assignee: Optional[UserRef] = None


class TicketRef(ORMBase):
    id: int
    title: str


# attachments
class AttachmentBase(ORMBase):
    filename: str
    filetype: str
    filesize: int
    uploaded_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AttachmentCreate(AttachmentBase):
    ticket_id: int


class AttachmentUpdate(ORMBase):
    ticket_id: Optional[int] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None
    filesize: Optional[int] = None


class AttachmentOut(AttachmentBase):
    id: int
    ticket: TicketRef


# messages
class MessageBase(ORMBase):
    content: str
    sent_at: Optional[datetime] = None
    edited_at: Optional[datetime] = None


class MessageCreate(MessageBase):
    sender_id: int
    receiver_id: int
    ticket_id: int


class MessageUpdate(ORMBase):
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    ticket_id: Optional[int] = None
    content: Optional[str] = None


class MessageOut(MessageBase):
    id: int
    sender: UserRef
    receiver: UserRef
    ticket: TicketRef

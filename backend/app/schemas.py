from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class ORMBase(BaseModel):
    class Config:
        orm_mode = True # for attr + dict access + model compatibility

# users
class UserBase(ORMBase):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(ORMBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserRef(ORMBase):
    id: int
    username: str


# tickets
class TicketBase(ORMBase):
    title: str
    status: str
    description: str
    category: Optional[str] = None

class TicketCreate(TicketBase):
    issuer_id: int
    assignee_id: Optional[int] = None

class TicketUpdate(ORMBase):
    issuer_id: Optional[int] = None
    assignee_id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    issuer: UserRef
    assignee: Optional[UserRef] = None
    created_at: datetime
    updated_at: datetime

class TicketRef(ORMBase):
    id: int
    title: str


# attachments
class AttachmentBase(ORMBase):
    filename: str
    filetype: str
    filesize: int

class AttachmentCreate(AttachmentBase):
    ticket_id: int

class AttachmentUpdate(ORMBase):
    ticket_id: Optional[int] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None
    filesize: Optional[int] = None

class AttachmentResponse(AttachmentBase):
    id: int
    ticket: TicketRef
    uploaded_at: datetime


# messages
class MessageBase(ORMBase):
    content: str

class MessageCreate(MessageBase):
    sender_id: int
    receiver_id: int
    ticket_id: int

class MessageUpdate(ORMBase):
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    ticket_id: Optional[int] = None
    content: Optional[str] = None

class MessageResponse(MessageBase):
    id: int
    sender: UserRef
    receiver: UserRef
    ticket: TicketRef
    sent_at: datetime
    edited_at: datetime



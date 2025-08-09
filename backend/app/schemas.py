from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class ORMBase(BaseModel):
    class Config:
        orm_mode = True

# users
class UserBase(ORMBase):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserUpdate(ORMBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserRef(ORMBase):
    id: int
    username: str


# tickets
class TicketBase(ORMBase):
    title: str
    status: str
    category: str
    description: Optional[str] = None

class TicketCreate(TicketBase):
    issuer_id: int
    assignee_id: Optional[int] = None

class TicketOut(TicketBase):
    id: int
    issuer_id: int
    assignee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TicketUpdate(ORMBase):
    title:  Optional[str] = None
    status:  Optional[str] = None
    category:  Optional[str] = None
    description: Optional[str] = None
    issuer_id:  Optional[int] = None
    assignee_id: Optional[int] = None

class TicketRef(ORMBase):
    id: int
    title: str


# attachments
class TicketAttachmentBase(ORMBase):
    filename: str
    size: int
    filetype: str

class TicketAttachmentCreate(TicketAttachmentBase):
    ticket_id: int

class TicketAttachmentOut(TicketAttachmentBase):
    id: int
    ticket_id: TicketRef
    uploaded_at: Optional[datetime] = None

class TicketAttachmentRef(ORMBase):
    id: int
    filename: str


# messages
class TicketMessageBase(ORMBase):
    content: str

class TicketMessageCreate(TicketMessageBase):
    ticket_id: int
    sender_id: int
    receiver_id: int

class TicketMessageOut(TicketMessageBase):
    id: int
    content: str
    ticket_id: TicketRef
    sender_id: UserRef
    receiver_id: UserRef
    sent_at: Optional[datetime] = None



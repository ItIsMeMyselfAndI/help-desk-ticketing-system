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
    description: Optional[str]

class TicketCreate(TicketBase):
    issue_id: int
    assigned_id: Optional[int]

class TicketOut(TicketBase):
    id: int
    issue_id: int
    assigned_id: Optional[int]
    create_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TicketUpdate(ORMBase):
    title:  Optional[str]
    status:  Optional[str]
    category:  Optional[str]
    description: Optional[str]
    issue_id:  Optional[str]
    assigned_id: Optional[int]

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



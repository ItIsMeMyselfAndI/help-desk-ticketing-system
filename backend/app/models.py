from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    attachment_id = Column(String, index=True)
    assignee_id = Column(Integer, index=True)
    message_id = Column(Integer, index=True)

class TicketAttachment(Base):
    __tablename__ = "ticket_attachments"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    size = Column(Integer, index=True)
    filetype = Column(String, index=True)
    uploaded_at = Column(DateTime, index=True)
    ticket_id = Column(Integer, index=True)

class TicketSupportAssignee(Base):
    __tablename__ = "ticket_support_assignees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String, index=True)
    ticket_id = Column(Integer, index=True)

class TicketMessage(Base):
    __tablename__ = "ticket_messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    sent_at = Column(DateTime, index=True)
    ticket_id = Column(Integer, index=True)
    sender_id = Column(Integer, index=True)
    receiver_id = Column(Integer, index=True)







from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional


# ---------- users ----------

def create_user(session: Session, user: schemas.UserCreate) -> models.User:
    if session.query(models.User).filter(models.User.username == user.username).first():
        raise ValueError("Username already exists.")
    if session.query(models.User).filter(models.User.email == user.email).first():
        raise ValueError("Email already exists.")
    db_user = models.User(
        username = user.username,
        email = user.email,
        password = user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session, limit: Optional[int]) -> List[models.User]:
    if limit == None:
        return session.query(models.User).all()
    return session.query(models.User).limit(limit).all()

def get_user(session: Session, user_id: int) -> Optional[models.User]:
    return session.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(session: Session, username: str) -> Optional[models.User]:
    return session.query(models.User).filter(models.User.username == username).first()

def update_user(session: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(session, user_id)
    if not db_user:
        return None
    updated_fields = user_update.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int) -> bool:
    db_user = get_user(session, user_id)
    if not db_user:
        return False
    session.delete(db_user)
    session.commit()
    return True


# ---------- ticket ----------

def create_ticket(session: Session, ticket: schemas.TicketCreate) -> models.Ticket:
    db_ticket = models.Ticket(
            title = ticket.title,
            status = ticket.status,
            category = ticket.category,
            description = ticket.description,
            issuer_id = ticket.issuer_id,
            assignee_id = ticket.assignee_id
            )
    session.add(db_ticket)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket

def get_tickets_for_user(session: Session, user_id: int,  limit: Optional[int]) -> List[models.Ticket]:
    if limit == None:
        return session.query(models.Ticket).filter(models.Ticket.issuer_id == user_id).all()
    return session.query(models.Ticket).filter(models.Ticket.issuer_id == user_id).limit(limit).all()

def get_ticket(session: Session, ticket_id: int) -> Optional[models.Ticket]:
    return session.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def update_ticket(session: Session, ticket_id: int, ticket_update: schemas.TicketUpdate) -> Optional[models.Ticket]:
    db_ticket = get_ticket(session, ticket_id)
    if not db_ticket:
        return None
    updated_fields = ticket_update.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        setattr(db_ticket, key, value)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket

def delete_ticket(session: Session, ticket_id: int) -> bool:
    db_ticket = get_ticket(session, ticket_id)
    if not db_ticket:
        return False
    session.delete(db_ticket)
    session.commit()
    return True


# ---------- ticket attachments ----------

def create_ticket_attachment(session: Session, ticket_attachment: schemas.TicketAttachmentCreate) -> models.TicketAttachment:
    db_ticket_attachment = models.TicketAttachment(
            filename = ticket_attachment.filename,
            size = ticket_attachment.size,
            filetype = ticket_attachment.filetype,
            ticket_id = ticket_attachment.ticket_id
            )
    session.add(db_ticket_attachment)
    session.commit()
    session.refresh(db_ticket_attachment)
    return db_ticket_attachment

def get_attachments_for_ticket(session: Session, ticket_id: int,  limit: Optional[int]) -> List[models.TicketAttachment]:
    if limit == None:
        return session.query(models.TicketAttachment).filter(models.TicketAttachment.ticket_id == ticket_id).all()
    return session.query(models.TicketAttachment).filter(models.TicketAttachment.ticket_id == ticket_id).limit(limit).all()

def get_ticket_attachment(session: Session, ticket_attachment_id: int) -> Optional[models.TicketAttachment]:
    return session.query(models.TicketAttachment).filter(models.TicketAttachment.id == ticket_attachment_id).first()

def delete_ticket_attachment(session: Session, ticket_attachment_id: int) -> bool:
    db_ticket_attachment = get_ticket_attachment(session, ticket_attachment_id)
    if not db_ticket_attachment:
        return False
    session.delete(db_ticket_attachment)
    session.commit()
    return True


# ---------- ticket messages ----------

def create_ticket_message(session: Session, ticket_message: schemas.TicketMessageCreate) -> models.TicketMessage:
    db_ticket_message = models.TicketMessage(
            content = ticket_message.content,
            ticket_id = ticket_message.ticket_id,
            sender_id = ticket_message.sender_id,
            receiver_id = ticket_message.receiver_id
            )
    session.add(db_ticket_message)
    session.commit()
    session.refresh(db_ticket_message)
    return db_ticket_message

def get_messages_for_ticket(session: Session, ticket_id: int,  limit: Optional[int]) -> List[models.TicketMessage]:
    if limit == None:
        return session.query(models.TicketMessage).filter(models.TicketMessage.ticket_id == ticket_id).all()
    return session.query(models.TicketMessage).filter(models.TicketMessage.ticket_id == ticket_id).limit(limit).all()

def get_ticket_message(session: Session, ticket_message_id: int) -> Optional[models.TicketMessage]:
    return session.query(models.TicketMessage).filter(models.TicketMessage.id == ticket_message_id).first()

def delete_ticket_message(session: Session, ticket_message_id: int) -> bool:
    db_ticket_message = get_ticket_message(session, ticket_message_id)
    if not db_ticket_message:
        return False
    session.delete(db_ticket_message)
    session.commit()
    return True




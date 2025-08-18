from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas


# users
def get_user_bad(db: Session, user_id: int):
    return db.get(models.User, user_id)

def create_user(db: Session, user: schemas.UserCreate) -> Optional[models.User]:
    user_exist = db.execute(select(models.User).where(models.User.username == user.username)).first()
    if user_exist:
        return None
    # ---- temporary ----
    user_dict = dict()
    for key, val in user.model_dump().items():
        if key == "password":
            key = "hashed_password"
        user_dict.update({key:val})
    # -------------------
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    return new_user

def update_user(db: Session, user_id: int,
                updated_user: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user_bad(db, user_id)
    if not db_user:
        return None
    updated_dict = updated_user.model_dump()
    for key, val in updated_dict.items():
        setattr(db_user, key, val)
    db.commit()
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    db_user = get_user_bad(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


# tickets
def get_ticket_bad(db: Session, ticket_id: int):
    return db.get(models.Ticket, ticket_id)

def create_ticket(db: Session, ticket: schemas.TicketCreate) -> Optional[models.Ticket]:
    ticket_dict = ticket.model_dump()
    new_ticket = models.Ticket(**ticket_dict)
    db.add(new_ticket)
    db.commit()
    return new_ticket

def update_ticket(db: Session, ticket_id: int,
                  updated_ticket: schemas.TicketUpdate) -> Optional[models.Ticket]:
    db_ticket = get_ticket_bad(db, ticket_id)
    if not db_ticket:
        return None
    updated_dict = updated_ticket.model_dump()
    for key, val in updated_dict.items():
        setattr(db_ticket, key, val)
    db.commit()
    return db_ticket

def delete_ticket(db: Session, ticket_id: int) -> Optional[models.Ticket]:
    db_ticket =  db.get(models.Ticket, ticket_id)
    db.delete(db_ticket)
    db.commit()
    return db_ticket


# attachments
def get_attachment_bad(db: Session, attachment_id: int):
    return db.get(models.Attachment, attachment_id)

def create_attachment(db: Session, attachment: schemas.AttachmentCreate) -> Optional[models.Attachment]:
    attachment_dict = attachment.model_dump()
    new_attachment = models.Attachment(**attachment_dict)
    db.add(new_attachment)
    db.commit()
    return new_attachment

def update_attachment(db: Session, attachment_id: int,
                  updated_attachment: schemas.AttachmentUpdate) -> Optional[models.Attachment]:
    db_attachment = get_attachment_bad(db, attachment_id)
    if not db_attachment:
        return None
    updated_dict = updated_attachment.model_dump()
    for key, val in updated_dict.items():
        setattr(db_attachment, key, val)
    db.commit()
    return db_attachment

def delete_attachment(db: Session, attachment_id: int) -> Optional[models.Attachment]:
    db_attachment = get_attachment_bad(db, attachment_id)
    db.delete(db_attachment)
    db.commit()
    return db_attachment


# messages
def get_message_bad(db: Session, message_id: int):
    return db.get(models.Message, message_id)

def create_message(db: Session, message: schemas.MessageCreate) -> Optional[models.Message]:
    message_dict = message.model_dump()
    new_message = models.Message(**message_dict)
    db.add(new_message)
    db.commit()
    return new_message

def update_message(db: Session, message_id: int,
                  updated_message: schemas.MessageUpdate) -> Optional[models.Message]:
    db_message = get_message_bad(db, message_id)
    if not db_message:
        return None
    updated_dict = updated_message.model_dump()
    for key, val in updated_dict.items():
        setattr(db_message, key, val)
    db.commit()
    return db_message

def delete_message(db: Session, message_id: int) -> Optional[models.Message]:
    db_message = get_message_bad(db, message_id)
    db.delete(db_message)
    db.commit()
    return db_message



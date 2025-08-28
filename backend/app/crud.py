from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, Tuple

from app.constants import Error

from . import models, schemas, security

# users
def verify_user_account(db: Session, username: str, password: str) -> bool:
    result = db.execute(select(models.User).where(models.User.username == username)).first()
    if not result:
        return False
    user: models.User = result[0]
    if security.verify_password(password, user.hashed_password):
        return True
    return False

def verify_user_id(db: Session, user_id: int) -> bool:
    result = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
    if result:
        return True
    return False

def get_user_good(db: Session, user_id: int) -> Tuple[Optional[schemas.UserOut], Error]:
    db_user = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
    if not db_user:
        return None, Error.USER_NOT_FOUND
    user_out = schemas.UserOut(**db_user.as_dict())
    return user_out, Error.SUCCESS

def create_user(db: Session, user: schemas.UserCreate) -> Tuple[Optional[models.User], Error]:
    uname_exist = db.execute(select(models.User).where(models.User.username == user.username)).first()
    email_exist = db.execute(select(models.User).where(models.User.email == user.email)).first()
    if uname_exist:
        return None, Error.UNAME_ALREADY_EXIST
    if email_exist:
        return None, Error.EMAIL_ALREADY_EXIST
    user_dict = dict()
    for key, val in user.model_dump().items():
        if key == "password":
            key = "hashed_password"
            val = security.hash_password(val)
        user_dict.update({key:val})
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    return new_user, Error.SUCCESS

def update_user(db: Session, user_id: int,
                updated_user: schemas.UserUpdate) -> Tuple[Optional[models.User], Error]:
    uname_exist = db.execute(select(models.User).where(models.User.username == updated_user.username)).first()
    email_exist = db.execute(select(models.User).where(models.User.email == updated_user.email)).first()
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None, Error.USER_NOT_FOUND
    elif uname_exist:
        return None, Error.UNAME_ALREADY_EXIST
    elif email_exist:
        return None, Error.EMAIL_ALREADY_EXIST
    updated_dict = updated_user.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_user, key, val)
    db.commit()
    return db_user, Error.SUCCESS

def delete_user(db: Session, user_id: int) -> Tuple[Optional[models.User], Error]:
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None, Error.USER_NOT_FOUND
    db.delete(db_user)
    db.commit()
    return db_user, Error.SUCCESS


# tickets
def get_ticket_good(db: Session, ticket_id: int) -> Tuple[Optional[schemas.TicketOut], Error]:
    db_ticket = db.execute(select(models.Ticket).where(models.Ticket.id == ticket_id)).scalars().first()
    if not db_ticket:
        return None, Error.TICKET_NOT_FOUND
    issuer = db.execute(select(models.User).where(models.User.id == db_ticket.issuer_id)).scalars().first()
    assignee = db.execute(select(models.User).where(models.User.id == db_ticket.assignee_id)).scalars().first()
    if not issuer:
        return None, Error.ISSUER_NOT_FOUND
    issuer_uname = issuer.username
    ticket_dict = db_ticket.as_dict()
    ticket_dict.update({
        "issuer": schemas.UserRef(
            id=ticket_dict["issuer_id"],
            username=issuer_uname
            ),
        })
    if assignee:
        ticket_dict.update({
            "assignee": schemas.UserRef(
                id=ticket_dict["assignee_id"],
                username=assignee.username
                )
            })
    ticket_out = schemas.TicketOut(**ticket_dict)
    return ticket_out, Error.SUCCESS

def create_ticket(db: Session, ticket: schemas.TicketCreate) -> Tuple[Optional[models.Ticket], Error]:
    # verify
    issuer_exist = verify_user_id(db, ticket.issuer_id)
    if not issuer_exist:
        return None, Error.ISSUER_NOT_FOUND
    if ticket.assignee_id != None:
        assignee_exist = verify_user_id(db, ticket.assignee_id)
        if not assignee_exist:
            return None, Error.ASSIGNEE_NOT_FOUND
    if ticket.issuer_id == ticket.assignee_id:
        return None, Error.SAME_ISSUER_AND_ASSIGNEE
    # main
    ticket_dict = ticket.model_dump()
    new_ticket = models.Ticket(**ticket_dict)
    db.add(new_ticket)
    db.commit()
    return new_ticket, Error.SUCCESS

def update_ticket(db: Session, ticket_id: int,
                  updated_ticket: schemas.TicketUpdate) -> Tuple[Optional[models.Ticket], Error]:
    # verify
    if updated_ticket.issuer_id != None:
        issuer_exist = verify_user_id(db, updated_ticket.issuer_id)
        if not issuer_exist:
            return None, Error.ISSUER_NOT_FOUND
    if updated_ticket.assignee_id != None:
        assignee_exist = verify_user_id(db, updated_ticket.assignee_id)
        if not assignee_exist:
            return None, Error.ASSIGNEE_NOT_FOUND
    if updated_ticket.issuer_id == updated_ticket.assignee_id:
        return None, Error.SAME_ISSUER_AND_ASSIGNEE
    # main
    db_ticket = db.get(models.Ticket, ticket_id)
    if not db_ticket:
        return None, Error.TICKET_NOT_FOUND
    updated_dict = updated_ticket.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_ticket, key, val)
    db.commit()
    return db_ticket, Error.SUCCESS

def delete_ticket(db: Session, ticket_id: int) -> Tuple[Optional[models.Ticket], Error]:
    db_ticket = db.get(models.Ticket, ticket_id)
    if not db_ticket:
        return None, Error.TICKET_NOT_FOUND
    db.delete(db_ticket)
    db.commit()
    return db_ticket, Error.SUCCESS


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
    updated_dict = updated_attachment.model_dump(exclude_none=True, exclude_unset=True)
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
    updated_dict = updated_message.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_message, key, val)
    db.commit()
    return db_message

def delete_message(db: Session, message_id: int) -> Optional[models.Message]:
    db_message = get_message_bad(db, message_id)
    db.delete(db_message)
    db.commit()
    return db_message



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
    result = db.get(models.Attachment, user_id)
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
def verify_ticket_id(db: Session, ticket_id: int) -> bool:
    result = db.get(models.Ticket, ticket_id)
    if result:
        return True
    return False

def get_ticket_good(db: Session, ticket_id: int) -> Tuple[Optional[schemas.TicketOut], Error]:
    db_ticket = db.execute(select(models.Ticket).where(models.Ticket.id == ticket_id)).scalars().first()
    if not db_ticket:
        return None, Error.TICKET_NOT_FOUND
    issuer = db.get(models.User, db_ticket.issuer_id)
    assignee = db.get(models.User, db_ticket.assignee_id)
    if not issuer:
        return None, Error.ISSUER_NOT_FOUND
    ticket_dict = db_ticket.as_dict()
    ticket_dict.update({
        "issuer": schemas.UserRef(
            id=ticket_dict["issuer_id"],
            username=issuer.username
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
def check_attachment_existence(db: Session, ticket_id: int, filename: str, filetype: str) -> bool:
    db_file = db.execute(select(models.Attachment).where(
        models.Ticket.id == ticket_id,
        models.Attachment.filename == filename,
        models.Attachment.filetype == filetype
        )).scalars().first()
    if db_file:
        return True
    return False

def verify_attachment_id(db: Session, attachment_id: int) -> bool:
    result = db.get(models.Attachment, attachment_id)
    if result:
        return True
    return False

def get_attachment_good(db: Session, attachment_id: int) -> Tuple[Optional[schemas.AttachmentOut], Error]:
    db_attachment = db.execute(select(models.Attachment).where(models.Attachment.id == attachment_id)).scalars().first()
    if not db_attachment:
        return None, Error.FILE_NOT_FOUND
    ticket = db.get(models.Ticket, db_attachment.ticket_id)
    if not ticket:
        return None, Error.TICKET_NOT_FOUND
    attachment_dict = db_attachment.as_dict()
    attachment_dict.update({
        "ticket": schemas.TicketRef(
            id=attachment_dict["ticket_id"],
            title=ticket.title
            ),
        })
    attachment_out = schemas.AttachmentOut(**attachment_dict)
    return attachment_out, Error.SUCCESS

def create_attachment(db: Session, attachment: schemas.AttachmentCreate) -> Tuple[Optional[models.Attachment], Error]:
    # verify
    ticket_exist = verify_ticket_id(db, attachment.ticket_id)
    if not ticket_exist:
        return None, Error.TICKET_NOT_FOUND
    file_exist = check_attachment_existence(db, attachment.ticket_id, attachment.filename, attachment.filetype)
    if file_exist:
        return None, Error.FILE_ALREADY_EXIST
    # main
    attachment_dict = attachment.model_dump()
    new_attachment = models.Attachment(**attachment_dict)
    db.add(new_attachment)
    db.commit()
    return new_attachment, Error.SUCCESS

def update_attachment(db: Session, attachment_id: int,
                  updated_attachment: schemas.AttachmentUpdate) -> Tuple[Optional[models.Attachment], Error]:
    # verify
    if updated_attachment.ticket_id != None:
        ticket_exist = verify_ticket_id(db, updated_attachment.ticket_id)
        if not ticket_exist:
            return None, Error.TICKET_NOT_FOUND
    # main
    db_attachment = db.get(models.Attachment, attachment_id)
    if not db_attachment:
        return None, Error.FILE_NOT_FOUND
    updated_dict = updated_attachment.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_attachment, key, val)
    db.commit()
    return db_attachment, Error.SUCCESS

def delete_attachment(db: Session, attachment_id: int) -> Tuple[Optional[models.Attachment], Error]:
    db_attachment = db.get(models.Attachment, attachment_id)
    if not db_attachment:
        return None, Error.FILE_NOT_FOUND
    db.delete(db_attachment)
    db.commit()
    return db_attachment, Error.SUCCESS


# messages
def verify_message_id(db: Session, message_id: int) -> bool:
    result = db.get(models.Message, message_id)
    if result:
        return True
    return False

def get_message_good(db: Session, message_id: int) -> Tuple[Optional[schemas.MessageOut], Error]:
    db_message = db.execute(select(models.Message).where(models.Message.id == message_id)).scalars().first()
    if not db_message:
        return None, Error.MESSAGE_NOT_FOUND
    ticket = db.get(models.Ticket, db_message.ticket_id)
    if not ticket:
        return None, Error.TICKET_NOT_FOUND
    sender = db.get(models.User, db_message.sender_id)
    if not sender:
        return None, Error.SENDER_NOT_FOUND
    receiver = db.get(models.User, db_message.receiver_id)
    if not receiver:
        return None, Error.RECEIVER_NOT_FOUND
    message_dict = db_message.as_dict()
    message_dict.update({
        "ticket": schemas.TicketRef(
            id=message_dict["ticket_id"],
            title=ticket.title
            ),
        })
    message_dict.update({
        "sender": schemas.UserRef(
            id=message_dict["sender_id"],
            username=sender.username
            ),
        })
    message_dict.update({
        "receiver": schemas.UserRef(
            id=message_dict["receiver_id"],
            username=receiver.username
            ),
        })
    message_out = schemas.MessageOut(**message_dict)
    return message_out, Error.SUCCESS

def create_message(db: Session, message: schemas.MessageCreate) -> Tuple[Optional[models.Message], Error]:
    # verify
    if message.content:
        return None, Error.CONTENT_IS_EMPTY
    ticket_exist = verify_ticket_id(db, message.ticket_id)
    if not ticket_exist:
        return None, Error.TICKET_NOT_FOUND
    sender_exist = verify_user_id(db, message.sender_id)
    if not sender_exist:
        return None, Error.SENDER_NOT_FOUND
    receiver_exist = verify_user_id(db, message.receiver_id)
    if not receiver_exist:
        return None, Error.RECEIVER_NOT_FOUND
    # main
    message_dict = message.model_dump()
    new_message = models.Message(**message_dict)
    db.add(new_message)
    db.commit()
    return new_message, Error.SUCCESS

def update_message(db: Session, message_id: int,
                  updated_message: schemas.MessageUpdate) -> Tuple[Optional[models.Message], Error]:
    # verify
    if updated_message.ticket_id != None:
        ticket_exist = verify_ticket_id(db, updated_message.ticket_id)
        if not ticket_exist:
            return None, Error.TICKET_NOT_FOUND
    if updated_message.sender_id != None:
        sender_exist = verify_user_id(db, updated_message.sender_id)
        if not sender_exist:
            return None, Error.SENDER_NOT_FOUND
    if updated_message.receiver_id != None:
        receiver_exist = verify_user_id(db, updated_message.receiver_id)
        if not receiver_exist:
            return None, Error.RECEIVER_NOT_FOUND
    # main
    db_message = db.get(models.Message, message_id)
    if not db_message:
        return None, Error.MESSAGE_NOT_FOUND
    updated_dict = updated_message.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_message, key, val)
    db.commit()
    return db_message, Error.SUCCESS

def delete_message(db: Session, message_id: int) -> Tuple[Optional[models.Message], Error]:
    db_message = db.get(models.Message, message_id)
    if not db_message:
        return None, Error.MESSAGE_NOT_FOUND
    db.delete(db_message)
    db.commit()
    return db_message, Error.SUCCESS

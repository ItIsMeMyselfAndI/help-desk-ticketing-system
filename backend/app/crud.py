import pydantic
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, Tuple

from app.constants import StatusCode
from app import models, schemas, security


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def check_same_ids(id_1: int, id_2) -> bool:
    return id_1 == id_2


# TODO: prevent assigning client as assignee
# [DONE] TODO-2: add try catch for invalid type args


# users
@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def verify_user_account(db: Session, username: str, password: str) -> bool:
    result = db.execute(
        select(models.User).where(models.User.username == username)
    ).first()
    if not result:
        return False
    user: models.User = result[0]
    if security.verify_password(password, user.hashed_password):
        return True
    return False


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def verify_user_id(db: Session, user_id: int) -> bool:
    result = db.get(models.User, user_id)
    if result:
        return True
    return False


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def get_user_good(
    db: Session, user_id: int
) -> Tuple[Optional[schemas.UserOut], StatusCode]:
    db_user = (
        db.execute(select(models.User).where(models.User.id == user_id))
        .scalars()
        .first()
    )
    if not db_user:
        return None, StatusCode.USER_NOT_FOUND
    user_out = schemas.UserOut.model_validate(db_user)
    return user_out, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def create_user(
    db: Session, user: schemas.UserCreate
) -> Tuple[Optional[models.User], StatusCode]:
    uname_exist = db.execute(
        select(models.User).where(models.User.username == user.username)
    ).first()
    email_exist = db.execute(
        select(models.User).where(models.User.email == user.email)
    ).first()
    if uname_exist:
        return None, StatusCode.UNAME_ALREADY_EXIST
    if email_exist:
        return None, StatusCode.EMAIL_ALREADY_EXIST
    user_dict = dict()
    for key, val in user.model_dump().items():
        if key == "password":
            key = "hashed_password"
            val = security.hash_password(val)
        user_dict.update({key: val})
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    return new_user, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def update_user(
    db: Session, user_id: int, updated_user: schemas.UserUpdate
) -> Tuple[Optional[models.User], StatusCode]:
    # verify
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None, StatusCode.USER_NOT_FOUND
    uname_exist = db.execute(
        select(models.User).where(models.User.username == updated_user.username)
    ).first()
    email_exist = db.execute(
        select(models.User).where(models.User.email == updated_user.email)
    ).first()
    if uname_exist:
        return None, StatusCode.UNAME_ALREADY_EXIST
    elif email_exist:
        return None, StatusCode.EMAIL_ALREADY_EXIST
    # main
    updated_dict = updated_user.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_user, key, val)
    db.commit()
    return db_user, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def delete_user(db: Session, user_id: int) -> Tuple[Optional[models.User], StatusCode]:
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None, StatusCode.USER_NOT_FOUND
    db.delete(db_user)
    db.commit()
    return db_user, StatusCode.SUCCESS


# tickets
@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def verify_ticket_id(db: Session, ticket_id: int) -> bool:
    result = db.get(models.Ticket, ticket_id)
    if result:
        return True
    return False


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def get_ticket_good(
    db: Session, ticket_id: int
) -> Tuple[Optional[schemas.TicketOut], StatusCode]:
    db_ticket = db.get(models.Ticket, ticket_id)
    if not db_ticket:
        return None, StatusCode.TICKET_NOT_FOUND
    issuer = db.get(models.User, db_ticket.issuer_id)
    assignee = db.get(models.User, db_ticket.assignee_id)
    if not issuer:
        return None, StatusCode.ISSUER_NOT_FOUND
    ticket_dict = db_ticket.as_dict()
    ticket_dict.update(
        {
            "issuer": schemas.UserRef(
                id=ticket_dict["issuer_id"], username=issuer.username
            ),
        }
    )
    if assignee:
        ticket_dict.update(
            {
                "assignee": schemas.UserRef(
                    id=ticket_dict["assignee_id"], username=assignee.username
                )
            }
        )
    ticket_out = schemas.TicketOut.model_validate(ticket_dict)
    return ticket_out, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def create_ticket(
    db: Session, ticket: schemas.TicketCreate
) -> Tuple[Optional[models.Ticket], StatusCode]:
    # verify
    issuer_exist = verify_user_id(db, ticket.issuer_id)
    if not issuer_exist:
        return None, StatusCode.ISSUER_NOT_FOUND
    if ticket.assignee_id != None:
        assignee_exist = verify_user_id(db, ticket.assignee_id)
        if not assignee_exist:
            return None, StatusCode.ASSIGNEE_NOT_FOUND
    if ticket.issuer_id == ticket.assignee_id:
        return None, StatusCode.SAME_ISSUER_AND_ASSIGNEE
    # main
    ticket_dict = ticket.model_dump()
    new_ticket = models.Ticket(**ticket_dict)
    db.add(new_ticket)
    db.commit()
    return new_ticket, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def update_ticket(
    db: Session, ticket_id: int, updated_ticket: schemas.TicketUpdate
) -> Tuple[Optional[models.Ticket], StatusCode]:
    # verify
    db_ticket = db.get(models.Ticket, ticket_id)
    if not db_ticket:
        return None, StatusCode.TICKET_NOT_FOUND
    if updated_ticket.issuer_id != None and updated_ticket.assignee_id != None:
        if updated_ticket.issuer_id == updated_ticket.assignee_id:
            return None, StatusCode.SAME_ISSUER_AND_ASSIGNEE
        issuer = db.get(models.Ticket, updated_ticket.issuer_id)
        assignee = db.get(models.Ticket, updated_ticket.assignee_id)
        if issuer == None:
            return None, StatusCode.ISSUER_NOT_FOUND
        if assignee == None:
            return None, StatusCode.ASSIGNEE_NOT_FOUND
    elif updated_ticket.issuer_id != None:
        issuer = db.get(models.Ticket, updated_ticket.issuer_id)
        if issuer == None:
            return None, StatusCode.ISSUER_NOT_FOUND
        if issuer.id == db_ticket.assignee_id:
            return None, StatusCode.SAME_ISSUER_AND_ASSIGNEE
    elif updated_ticket.assignee_id != None:
        assignee = db.get(models.Ticket, updated_ticket.assignee_id)
        if assignee == None:
            return None, StatusCode.ASSIGNEE_NOT_FOUND
        if assignee.id == db_ticket.issuer_id:
            return None, StatusCode.SAME_ISSUER_AND_ASSIGNEE
    # main
    updated_dict = updated_ticket.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_ticket, key, val)
    db.commit()
    return db_ticket, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def delete_ticket(
    db: Session, ticket_id: int
) -> Tuple[Optional[models.Ticket], StatusCode]:
    db_ticket = db.get(models.Ticket, ticket_id)
    if not db_ticket:
        return None, StatusCode.TICKET_NOT_FOUND
    db.delete(db_ticket)
    db.commit()
    return db_ticket, StatusCode.SUCCESS


# attachments
@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def check_attachment_existence(
    db: Session, ticket_id: int, filename: str, filetype: str
) -> bool:
    db_file = (
        db.execute(
            select(models.Attachment).where(
                models.Ticket.id == ticket_id,
                models.Attachment.filename == filename,
                models.Attachment.filetype == filetype,
            )
        )
        .scalars()
        .first()
    )
    if db_file:
        return True
    return False


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def verify_attachment_id(db: Session, attachment_id: int) -> bool:
    result = db.get(models.Attachment, attachment_id)
    if result:
        return True
    return False


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def get_attachment_good(
    db: Session, attachment_id: int
) -> Tuple[Optional[schemas.AttachmentOut], StatusCode]:
    db_attachment = db.get(models.Attachment, attachment_id)
    if not db_attachment:
        return None, StatusCode.FILE_NOT_FOUND
    ticket = db.get(models.Ticket, db_attachment.ticket_id)
    if not ticket:
        return None, StatusCode.TICKET_NOT_FOUND
    attachment_dict = db_attachment.as_dict()
    attachment_dict.update(
        {
            "ticket": schemas.TicketRef(
                id=attachment_dict["ticket_id"], title=ticket.title
            ),
        }
    )
    attachment_out = schemas.AttachmentOut.model_validate(attachment_dict)
    return attachment_out, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def create_attachment(
    db: Session, attachment: schemas.AttachmentCreate
) -> Tuple[Optional[models.Attachment], StatusCode]:
    # verify
    ticket_exist = verify_ticket_id(db, attachment.ticket_id)
    if not ticket_exist:
        return None, StatusCode.TICKET_NOT_FOUND
    file_exist = check_attachment_existence(
        db, attachment.ticket_id, attachment.filename, attachment.filetype
    )
    if file_exist:
        return None, StatusCode.FILE_ALREADY_EXIST
    # main
    attachment_dict = attachment.model_dump()
    new_attachment = models.Attachment(**attachment_dict)
    db.add(new_attachment)
    db.commit()
    return new_attachment, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def update_attachment(
    db: Session, attachment_id: int, updated_attachment: schemas.AttachmentUpdate
) -> Tuple[Optional[models.Attachment], StatusCode]:
    # verify
    db_attachment = db.get(models.Attachment, attachment_id)
    if not db_attachment:
        return None, StatusCode.FILE_NOT_FOUND
    if updated_attachment.ticket_id != None:
        ticket_exist = verify_ticket_id(db, updated_attachment.ticket_id)
        if not ticket_exist:
            return None, StatusCode.TICKET_NOT_FOUND
    # main
    updated_dict = updated_attachment.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_attachment, key, val)
    db.commit()
    return db_attachment, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def delete_attachment(
    db: Session, attachment_id: int
) -> Tuple[Optional[models.Attachment], StatusCode]:
    db_attachment = db.get(models.Attachment, attachment_id)
    if not db_attachment:
        return None, StatusCode.FILE_NOT_FOUND
    db.delete(db_attachment)
    db.commit()
    return db_attachment, StatusCode.SUCCESS


# messages
@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def verify_message_id(db: Session, message_id: int) -> bool:
    result = db.get(models.Message, message_id)
    if result:
        return True
    return False


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def get_message_good(
    db: Session, message_id: int
) -> Tuple[Optional[schemas.MessageOut], StatusCode]:
    db_message = db.get(models.Message, message_id)
    if not db_message:
        return None, StatusCode.MESSAGE_NOT_FOUND
    ticket = db.get(models.Ticket, db_message.ticket_id)
    if not ticket:
        return None, StatusCode.TICKET_NOT_FOUND
    sender = db.get(models.User, db_message.sender_id)
    if not sender:
        return None, StatusCode.SENDER_NOT_FOUND
    receiver = db.get(models.User, db_message.receiver_id)
    if not receiver:
        return None, StatusCode.RECEIVER_NOT_FOUND
    message_dict = db_message.as_dict()
    message_dict.update(
        {
            "ticket": schemas.TicketRef(
                id=message_dict["ticket_id"], title=ticket.title
            ),
        }
    )
    message_dict.update(
        {
            "sender": schemas.UserRef(
                id=message_dict["sender_id"], username=sender.username
            ),
        }
    )
    message_dict.update(
        {
            "receiver": schemas.UserRef(
                id=message_dict["receiver_id"], username=receiver.username
            ),
        }
    )
    message_out = schemas.MessageOut.model_validate(message_dict)
    return message_out, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def create_message(
    db: Session, message: schemas.MessageCreate
) -> Tuple[Optional[models.Message], StatusCode]:
    # verify
    if not message.content:
        return None, StatusCode.CONTENT_IS_EMPTY
    ticket_exist = verify_ticket_id(db, message.ticket_id)
    if not ticket_exist:
        return None, StatusCode.TICKET_NOT_FOUND
    sender = db.get(models.User, message.sender_id)
    if not sender:
        return None, StatusCode.SENDER_NOT_FOUND
    receiver = db.get(models.User, message.receiver_id)
    if not receiver:
        return None, StatusCode.RECEIVER_NOT_FOUND
    if check_same_ids(sender.id, receiver.id):
        return None, StatusCode.SAME_SENDER_AND_RECEIVER
    # main
    message_dict = message.model_dump()
    new_message = models.Message(**message_dict)
    db.add(new_message)
    db.commit()
    return new_message, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def update_message(
    db: Session, message_id: int, updated_message: schemas.MessageUpdate
) -> Tuple[Optional[models.Message], StatusCode]:
    # verify
    orig_message = db.get(models.Message, message_id)
    if not orig_message:
        return None, StatusCode.MESSAGE_NOT_FOUND
    if updated_message.ticket_id != None:
        ticket_exist = verify_ticket_id(db, updated_message.ticket_id)
        if not ticket_exist:
            return None, StatusCode.TICKET_NOT_FOUND
    if updated_message.sender_id != None:
        sender = db.get(models.User, updated_message.sender_id)
        if not sender:
            return None, StatusCode.SENDER_NOT_FOUND
        if check_same_ids(sender.id, orig_message.sender_id):
            return None, StatusCode.SAME_SENDER_AND_RECEIVER
    if updated_message.receiver_id != None:
        receiver = db.get(models.User, updated_message.receiver_id)
        if not receiver:
            return None, StatusCode.RECEIVER_NOT_FOUND
        if check_same_ids(receiver.id, orig_message.sender_id):
            return None, StatusCode.SAME_SENDER_AND_RECEIVER
    if updated_message.sender_id != None and updated_message.receiver_id != None:
        if check_same_ids(updated_message.sender_id, updated_message.receiver_id):
            return None, StatusCode.SAME_SENDER_AND_RECEIVER
    # main
    db_message = db.get(models.Message, message_id)
    if not db_message:
        return None, StatusCode.MESSAGE_NOT_FOUND
    updated_dict = updated_message.model_dump(exclude_none=True, exclude_unset=True)
    for key, val in updated_dict.items():
        setattr(db_message, key, val)
    db.commit()
    return db_message, StatusCode.SUCCESS


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
def delete_message(
    db: Session, message_id: int
) -> Tuple[Optional[models.Message], StatusCode]:
    db_message = db.get(models.Message, message_id)
    if not db_message:
        return None, StatusCode.MESSAGE_NOT_FOUND
    db.delete(db_message)
    db.commit()
    return db_message, StatusCode.SUCCESS

from typing import List, Literal, Optional
from sqlalchemy import create_engine, insert, select, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import user

from app import crud, schemas, constants
from .config import DATABASE_URL
import json

engine = create_engine(DATABASE_URL) # , echo=True
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    with Session() as session:
        # session.expire_on_commit = False
        yield session

def init_db(with_data: bool, datasets_path: Optional[str]):
    db_exists = inspect(engine).get_table_names()
    if db_exists:
        print("[*] Database already exists.")
        return
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("[*] Database initialized.")
    if with_data and not db_exists:
        if not datasets_path:
            return
        insert_data(datasets_path, "users")
        insert_data(datasets_path, "tickets")
        insert_data(datasets_path, "attachments")
        insert_data(datasets_path, "messages")

def drop_db():
    from app.models import Base
    Base.metadata.drop_all(bind=engine)
    print("[*] Database dropped.")


# ---- inserting sample data ----
def insert_data(datasets_path: str, tablename: constants.TableNamesLiterals):
    db = next(get_db())
    with open(datasets_path, "r") as file:
        dataset_json = json.load(file)
    if not dataset_json:
        print("no data")
        return None
    # create entries
    print(f"[*] Inserting {tablename.capitalize()}...")
    for i, entry in enumerate(dataset_json[tablename]):
        obj = None
        if tablename == "users":
            user = schemas.UserCreate(**entry)
            obj = crud.create_user(db, user)
        elif tablename == "tickets":
            ticket = schemas.TicketCreate(**entry)
            obj = crud.create_ticket(db, ticket)
        elif tablename == "attachments":
            attachment = schemas.AttachmentCreate(**entry)
            obj = crud.create_attachment(db, attachment)
        elif tablename == "messages":
            message = schemas.MessageCreate(**entry)
            obj = crud.create_message(db, message)
        print(f"\t [+] {{{i}}} {obj}")
    print(f"[*] {tablename.capitalize()} inserted.")





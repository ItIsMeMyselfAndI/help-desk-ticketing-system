from typing import Optional
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.constants import TableName
from app import crud, schemas
from app.config import DATABASE_URL
import json

engine = create_engine(DATABASE_URL)  # , echo=True
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
        print("closed db session")


def init_db(datasets_path: Optional[str] = None):
    db_exists = inspect(engine).get_table_names()
    if db_exists:
        print("[*] Database already exists.")
        return
    print("[*] Database initialized.")
    from app.models import Base

    Base.metadata.create_all(bind=engine)
    if not datasets_path:
        return
    insert_data(datasets_path, TableName.USERS)
    insert_data(datasets_path, TableName.TICKETS)
    insert_data(datasets_path, TableName.ATTACHMENTS)
    insert_data(datasets_path, TableName.MESSAGES)


def drop_db():
    from app.models import Base

    Base.metadata.drop_all(bind=engine)
    print("[*] Database dropped.")


def reset_db():
    drop_db()
    init_db()


# ---- inserting sample data ----
def insert_data(datasets_path: str, tablename: TableName):
    db = next(get_db())
    with open(datasets_path, "r") as file:
        try:
            dataset_json = json.load(file)
        except json.JSONDecodeError:
            print(f'[!] File "{datasets_path}" is not json')
            return
    if not dataset_json:
        print("no data")
        return None
    # create entries
    print(f"[*] Inserting {tablename.value.capitalize()}...")
    for i, entry in enumerate(dataset_json[tablename.value]):
        obj = None
        if tablename is TableName.USERS:
            user = schemas.UserCreate(**entry)
            obj = crud.create_user(db, user)
        elif tablename is TableName.TICKETS:
            ticket = schemas.TicketCreate(**entry)
            obj = crud.create_ticket(db, ticket)
        elif tablename is TableName.ATTACHMENTS:
            attachment = schemas.AttachmentCreate(**entry)
            obj = crud.create_attachment(db, attachment)
        elif tablename is TableName.MESSAGES:
            message = schemas.MessageCreate(**entry)
            obj = crud.create_message(db, message)
        print(f"\t [+] {{{i}}} {obj}")
    print(f"[*] {tablename.value.capitalize()} inserted.")


if __name__ == "__main__":
    import sys

    argv = sys.argv

    def print_usage():
        print(
            "Usage:\n",
            "\tdb.py --drop\n",
            "\tdb.py --init\n",
            "\tdb.py --reset\n",
            '\tdb.py --init --data "app/datasets.json"\n',
        )

    if len(argv) not in [2, 4]:
        print(len(argv))
        print("lkjl")
        print_usage()
    elif len(argv) == 2:
        if argv[1] == "--drop":
            drop_db()
        elif argv[1] == "--init":
            init_db()
        elif argv[1] == "--reset":
            reset_db()
        else:
            print_usage()
    elif len(argv) == 4:
        if argv[1] == "--init" and argv[2] == "--data":
            try:
                init_db(argv[3])
            except FileNotFoundError:
                print(f'File "{argv[3]}" not found.')
        else:
            print_usage()
    else:
        print_usage()

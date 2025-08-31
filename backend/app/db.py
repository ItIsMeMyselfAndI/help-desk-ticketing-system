from typing import Generator, Optional
from sqlalchemy import Connection, Engine, create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from app.constants import TableName
from app import crud, schemas
from app.config import DATABASE_URL
import json

engine = create_engine(DATABASE_URL)  # , echo=True
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
        print("closed db session")


def init_db(
    bind: Engine | Connection = engine,
    datasets_path: str | None = None,
    limit: int | None = None,
):
    db_exists = inspect(engine).get_table_names()
    if db_exists:
        print("[*] Database already exists.")
        return
    print("[*] Database initialized.")
    from app.models import Base

    Base.metadata.create_all(bind=bind)
    if not datasets_path:
        return
    insert_data(datasets_path, TableName.USERS, bind, limit)
    insert_data(datasets_path, TableName.TICKETS, bind, limit)
    insert_data(datasets_path, TableName.ATTACHMENTS, bind, limit)
    insert_data(datasets_path, TableName.MESSAGES, bind, limit)


def drop_db(bind: Engine | Connection = engine):
    from app.models import Base

    Base.metadata.drop_all(bind=bind)
    print("[*] Database dropped.")


def reset_db(
    bind: Engine | Connection = engine,
    datasets_path: Optional[str] = None,
    limit: int | None = None,
):
    drop_db(bind)
    init_db(bind, datasets_path, limit)


# ---- inserting sample data ----
def insert_data(
    datasets_path: str,
    tablename: TableName,
    bind: Engine | Connection = engine,
    limit: int | None = None,
):
    # local session maker
    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=bind)
    db = session_maker()

    try:
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
            if limit:
                if i == limit:
                    break

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

    finally:
        db.close()


if __name__ == "__main__":
    import sys

    argv = sys.argv

    def print_usage():
        print(
            "Usage:\n",
            "----------------------------------------------------------\n",
            "[Drop database]\n",
            "\tdb.py --drop\n",
            "[Initialize database]\n",
            "\tdb.py --init\n",
            '\tdb.py --init --data "app/datasets.json"\n',
            '\tdb.py --init --data "app/datasets.json" --limit 1\n',
            "[Reset database]\n",
            "\tdb.py --reset\n",
            '\tdb.py --reset --data "app/datasets.json"\n',
            '\tdb.py --reset --data "app/datasets.json" --limit 1\n',
        )

    if len(argv) not in [2, 4, 6]:
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
                init_db(datasets_path=argv[3])
            except FileNotFoundError:
                print(f'File "{argv[3]}" not found.')
        elif argv[1] == "--reset" and argv[2] == "--data":
            try:
                reset_db(datasets_path=argv[3])
            except FileNotFoundError:
                print(f'File "{argv[3]}" not found.')
        else:
            print_usage()
    elif len(argv) == 6:
        if argv[1] == "--init" and argv[2] == "--data" and argv[4] == "--limit":
            try:
                init_db(datasets_path=argv[3], limit=int(argv[5]))
            except FileNotFoundError:
                print(f'File "{argv[3]}" not found.')
            except ValueError:
                print(f'Limit "{argv[5]}" is not an integer.')
        elif argv[1] == "--reset" and argv[2] == "--data" and argv[4] == "--limit":
            try:
                reset_db(datasets_path=argv[3], limit=int(argv[5]))
            except FileNotFoundError:
                print(f'File "{argv[3]}" not found.')
            except ValueError:
                print(f'Limit "{argv[5]}" is not an integer.')
        else:
            print_usage()
    else:
        print_usage()

import json
from fastapi import FastAPI

from app import crud, models, schemas
from app.constants import Error
from app.db import get_db

paths = {
        "user": [
            "/user/{user_id:int}",
            "/user/?username={uname:str}&password={passwd:str}",
            ],
        "ticket": "",
        "attachment": "",
        "message": "",
        }

app = FastAPI()

@app.get("/")
def root():
    return {
            "app": "help desk ticketing system",
            "paths": paths
            }


# ---- users ----
@app.get("/user")
def verify_user(username: str, password: str):
    db = next(get_db())
    result = crud.verify_user_account(db, username, password)
    print(json.dumps({"verified": result}, indent=4))
    return {"verified": result}

@app.get("/user/{user_id}")
def get_user_good(user_id: int):
    db = next(get_db())
    result, status_code = crud.get_user_good(db, user_id)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    user_out = result.model_dump(mode="json")
    print(json.dumps(user_out, indent=4))
    return result

@app.post("/user/create")
def create_user(user: schemas.UserCreate):
    db = next(get_db())
    result, status_code = crud.create_user(db, user)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    user_out = result.as_dict()
    user_out.update({"role" : user_out["role"].value})
    print(json.dumps(user_out, indent=4))
    return user_out

@app.patch("/user/update/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdate):
    db = next(get_db())
    result, status_code = crud.update_user(db, user_id, user)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    user_out = result.as_dict()
    user_out.update({"role" : user_out["role"].value})
    print(json.dumps(user_out, indent=4))
    return user_out

@app.delete("/user/delete/{user_id}")
def delete_user(user_id: int):
    db = next(get_db())
    result, status_code = crud.delete_user(db, user_id)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    user_out = result.as_dict()
    user_out.update({"role" : user_out["role"].value})
    print(json.dumps(user_out, indent=4))
    return user_out


# ---- tickets ----
@app.get("/ticket/{ticket_id}")
def get_ticket_good(ticket_id: int):
    db = next(get_db())
    result, status_code = crud.get_ticket_good(db, ticket_id)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    ticket_out = result.model_dump(mode="json")
    print(json.dumps(ticket_out, indent=4))
    return result

@app.post("/ticket/create")
def create_ticket(ticket: schemas.TicketCreate):
    db = next(get_db())
    result, status_code = crud.create_ticket(db, ticket)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    ticket_out = result.as_dict()
    ticket_out.update({"status" : ticket_out["status"].value})
    if result.category:
        ticket_out.update({"category" : ticket_out["category"].value})
    print(json.dumps(ticket_out, indent=4))
    return ticket_out

@app.patch("/ticket/update/{ticket_id}")
def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate):
    db = next(get_db())
    result, status_code = crud.update_ticket(db, ticket_id, ticket)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    ticket_out = result.as_dict()
    ticket_out.update({"status" : ticket_out["status"].value})
    if result.category:
        ticket_out.update({"category" : ticket_out["category"].value})
    print(json.dumps(ticket_out, indent=4))
    return ticket_out

@app.delete("/ticket/delete/{ticket_id}")
def delete_ticket(ticket_id: int):
    db = next(get_db())
    result, status_code = crud.delete_ticket(db, ticket_id)
    if not result:
        print(json.dumps({"status_code": status_code.value}, indent=4))
        return {"status_code": status_code}
    ticket_out = result.as_dict()
    ticket_out.update({"status" : ticket_out["status"].value})
    if result.category:
        ticket_out.update({"category" : ticket_out["category"].value})
    print(json.dumps(ticket_out, indent=4))
    return ticket_out








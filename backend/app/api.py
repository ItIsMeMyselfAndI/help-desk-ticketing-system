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
    result = crud.verify_user(db, username, password)
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
    print(json.dumps(user_out, indent=4))
    return user_out







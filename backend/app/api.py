from fastapi import FastAPI
import json

from app import db, crud, schemas

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
    dbase = next(db.get_db())
    result = crud.verify_user(dbase, username, password)
    return {"verified": result}

@app.get("/user/{user_id}")
def get_user_bad(user_id: int):
    dbase = next(db.get_db())
    user = crud.get_user_bad(dbase, user_id)
    return user

@app.post("/user/create")
def create_user(user: schemas.UserCreate):
    dbase = next(db.get_db())
    result, err = crud.create_user(dbase, user)
    if not result:
        print(f"[!] {err}")
        return
    print(f"""
          username: {result.username}
          email: {result.email}
          hashed_password: {result.hashed_password}
          role: {result.role.value}
          created_at: {result.created_at}
          updated_at: {result.updated_at}
          """)

@app.patch("/user/update")
def update_user(user_id: int, user: schemas.UserUpdate):
    dbase = next(db.get_db())
    result, err = crud.update_user(dbase, user_id, user)
    if not result:
        print(f"[!] {err}")
        return
    print(f"""
          username: {result.username}
          email: {result.email}
          hashed_password: {result.hashed_password}
          role: {result.role.value}
          created_at: {result.created_at}
          updated_at: {result.updated_at}
          """)

@app.delete("/user/delete/{user_id}")
def delete_user(user_id: int):
    dbase = next(db.get_db())
    result, err = crud.delete_user(dbase, user_id)
    if not result:
        print(f"[!] {err}")
        return
    print(f"""
          username: {result.username}
          email: {result.email}
          hashed_password: {result.hashed_password}
          role: {result.role.value}
          created_at: {result.created_at}
          updated_at: {result.updated_at}
          """)







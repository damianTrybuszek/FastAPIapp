from typing import List
from uuid import uuid4

from fastapi import FastAPI

from models import User, Gender, Role

app = FastAPI()

db: List[User] = [
    User(id=uuid4(), first_name="Katy", last_name="Perry", gender=Gender.female, roles=[Role.student]),
    User(id=uuid4(), first_name="Zakk", last_name="Wylde", gender=Gender.male, roles=[Role.admin, Role.user])
]


@app.get("/")
async def root():
    return {"Hello": "Damian"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

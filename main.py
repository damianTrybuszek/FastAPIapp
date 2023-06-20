from typing import Optional, List
from uuid import UUID
from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel

import models
from database import SessionLocal
from models import Genre, Role

app = FastAPI()


class Musician(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    band: Optional[str] = "solo musician"
    genres: List[Genre]
    roles: List[Role]

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get("/api/v1/musicians", response_model=List[Musician], status_code=200)
async def get_all_musicians():
    musicians = db.query(models.Musician).all()
    return musicians


@app.get("/api/v1/musicians/{musician_id}")
async def get_an_musician(musician_id: UUID):
    pass


@app.post("/api/v1/musicians", response_model=Musician, status_code=status.HTTP_201_CREATED)
async def register_musician(musician: Musician):
    new_musician = models.Musician(
        id=musician.id,
        first_name=musician.first_name,
        last_name=musician.last_name,
        band=musician.band,
        genres=musician.genres,
        roles=musician.roles,
    )
    db.add(new_musician)
    db.commit()
    return new_musician


@app.put("/api/v1/musicians/{musician_id}")
async def modify_musician_details(musician_id: UUID):
    pass


@app.delete("/api/v1/musicians/{musician_id}")
async def delete_musician(musician_id: UUID):
    pass

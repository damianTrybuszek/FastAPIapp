from enum import Enum
from typing import Optional, List
from uuid import UUID
from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

import models
from database import SessionLocal


class Genre(str, Enum):
    rock = "rock"
    pop = "pop"
    jazz = "jazz"
    metal = "metal"
    hard_rock = "hard rock"
    heavy_metal = "heavy metal"


class Role(str, Enum):
    guitar_player = "guitar_player"
    bass_player = "bass player"
    keyboard_player = "keyboard_player"
    drummer = "drummer"
    vocalist = "vocalist"


class Musician(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    band: Optional[str] = "solo musician"
    genres: List[Genre]
    roles: List[Role]

    class Config:
        orm_mode = True


app = FastAPI()
db = SessionLocal()


@app.get("/api/v1/musicians", response_model=List[Musician], status_code=status.HTTP_200_OK)
async def get_all_musicians():
    musicians = db.query(models.Musician).all()
    return musicians


@app.get("/api/v1/musicians/{musician_id}", response_model=Musician, status_code=status.HTTP_200_OK)
async def get_a_musician(musician_id: UUID):
    return db.query(models.Musician).filter(models.Musician.id == musician_id).first()


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


@app.put("/api/v1/musicians/{musician_id}", response_model=Musician, status_code=status.HTTP_200_OK)
async def modify_musician_details(musician_id: UUID, musician: Musician):
    musician_to_update = db.query(models.Musician).filter(models.Musician.id == musician_id).first()
    musician_to_update.first_name = musician.first_name
    musician_to_update.last_name = musician.last_name
    musician_to_update.band = musician.band
    musician_to_update.genres = musician.genres
    musician_to_update.roles = musician.roles

    db.commit()

    return musician_to_update


@app.delete("/api/v1/musicians/{musician_id}")
async def delete_musician(musician_id: UUID):
    musician_to_delete = db.query(models.Musician).filter(models.Musician.id == musician_id).first()

    if musician_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Musician with given ID does not exist.")

    db.delete(musician_to_delete)
    db.commit()
    return musician_to_delete
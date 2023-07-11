from enum import Enum
from typing import Optional, List
from uuid import UUID
from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
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
    guitar_player = "guitar player"
    bass_player = "bass player"
    keyboard_player = "keyboard player"
    drummer = "drummer"
    vocalist = "vocalist"

class Roles(BaseModel):
    id: Optional[UUID] = uuid4()
    musician_id: Optional[UUID]
    role_name: Role

    class Config:
        orm_mode = True

class Genres(BaseModel):
    id: Optional[UUID] = uuid4()
    musician_id: Optional[UUID]
    genre_name: Genre

    class Config:
        orm_mode = True

class Musician(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    band: Optional[str] = "Solo musician"
    genres: List[Genres]
    roles: List[Roles]

    class Config:
        orm_mode = True


app = FastAPI()
db = SessionLocal()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)
db.query()


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
        id=uuid4(),
        first_name=musician.first_name,
        last_name=musician.last_name,
        band=musician.band
    )

    for new_genre in musician.genres:
        genre_to_create = models.Genres(
            id=uuid4(),
            musician_id=new_musician.id,
            genre_name=new_genre.genre_name,
        )
        db.add(genre_to_create)

    for new_role in musician.roles:
        role_to_create = models.Roles(
            id=uuid4(),
            musician_id=new_musician.id,
            role_name=new_role.role_name,
        )
        db.add(role_to_create)

    db.add(new_musician)
    db.commit()
    return new_musician



@app.put("/api/v1/musicians/{musician_id}", response_model=Musician, status_code=status.HTTP_200_OK)
async def modify_musician_details(musician_id: UUID, musician: Musician):
    musician_to_update = db.query(models.Musician).filter(models.Musician.id == musician_id).first()
    musician_to_update.first_name = musician.first_name
    musician_to_update.last_name = musician.last_name
    musician_to_update.band = musician.band

    for genre_to_delete in musician_to_update.genres:
        db.delete(genre_to_delete)

    for role_to_delete in musician_to_update.roles:
        db.delete(role_to_delete)

    for new_genre in musician.genres:
        genre_to_create = models.Genres(
            id=uuid4(),
            musician_id=musician_to_update.id,
            genre_name=new_genre.genre_name,
        )
        db.add(genre_to_create)

    for new_role in musician.roles:
        role_to_create = models.Roles(
            id=uuid4(),
            musician_id=musician_to_update.id,
            role_name=new_role.role_name,
        )
        db.add(role_to_create)

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
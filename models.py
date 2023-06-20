from enum import Enum

from sqlalchemy import String, Column, UUID, ARRAY

from database import Base


class Genre(str, Enum):
    rock = "rock"
    pop = "pop"
    jazz = "jazz"
    metal = "metal"
    hard_rock = "hard rock"
    heavy_metal = "heavy metal"


class Role(str, Enum):
    guitarist = "guitarist"
    bassist = "bassist"
    keyboardist = "keyboardist"
    drummer = "drummer"
    vocalist = "vocalist"


class Musician(Base):
    __tablename__ = "musicians"
    id = Column(UUID, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    band = Column(String(255))
    genres = Column(ARRAY(String))
    roles = Column(ARRAY(String))

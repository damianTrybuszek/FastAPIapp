from sqlalchemy import String, Column, UUID, ARRAY

from database import Base


class Musician(Base):
    __tablename__ = "musicians"
    id = Column(UUID, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    band = Column(String(255))
    genres = Column(ARRAY(String))
    roles = Column(ARRAY(String))

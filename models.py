from sqlalchemy import String, Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Musician(Base):
    __tablename__ = 'musicians'
    id = Column(UUID, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    band = Column(String)
    genres = relationship('Genres', backref='Musician', primaryjoin="Musician.id == Genres.musician_id")
    roles = relationship('Roles', backref='Musician', primaryjoin="Musician.id == Roles.musician_id")

class Roles(Base):
    __tablename__ = "roles"
    id = Column(UUID, primary_key=True)
    musician_id = Column(String, ForeignKey('musicians.id', ondelete='CASCADE'))
    role_name = Column(String)
    
class Genres(Base):
    __tablename__ = "genres"
    id = Column(UUID, primary_key=True)
    musician_id = Column(String, ForeignKey('musicians.id', ondelete='CASCADE'))
    genre_name = Column(String)

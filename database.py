from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

connection_url =

engine = create_engine(connection_url, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

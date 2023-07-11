import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

connection_url =os.getenv('DB_CONN_STR')

engine = sqlalchemy.create_engine(connection_url, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

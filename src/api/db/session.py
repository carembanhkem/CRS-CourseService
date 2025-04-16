import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL

engine = sqlmodel.create_engine(DATABASE_URL)

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

def init_db():
    print("creating database ...")
    print(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
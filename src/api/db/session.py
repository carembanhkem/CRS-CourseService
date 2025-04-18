import os
import json
import sqlmodel
from sqlmodel import SQLModel, Session, select
from sqlalchemy import inspect, text

from api.db.models import Hero
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


def is_heroes_table_empty_or_missing() -> bool:
    with Session(engine) as session:
        inspector = inspect(engine)
        if "heroes" not in inspector.get_table_names():
            return True  # Table doesn't exist

        result = session.execute(select(Hero).limit(1)).first()
        return result is None  # Table exists but is empty


def insert_heroes_from_json(file_path: str):
    if not os.path.exists(file_path):
        print(f"[WARN] File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    heroes = [Hero(**item) for item in data]

    with Session(engine) as session:
        session.add_all(heroes)
        session.commit()
        print(f"[INFO] Inserted {len(heroes)} heroes into the database.")

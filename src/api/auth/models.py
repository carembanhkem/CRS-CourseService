from enum import Enum
import uuid
from sqlmodel import Column, Field, SQLModel
import sqlalchemy.dialects.postgresql as pg
from typing import Optional


class UserType(str, Enum):
    INSTRUCTOR = "INSTRUCTOR"
    PLAYER = "PLAYER"


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str
    email: str
    cognito_sub: str
    role: str

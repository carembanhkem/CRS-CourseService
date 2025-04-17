from enum import Enum
import uuid
from sqlmodel import Column, Field, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from typing import Optional

from api.courses import models


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
    courses: list["models.CourseModel"] = Relationship( #this is a forward reference
        back_populates="instructor", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class SignupRequestSchema(SQLModel):
    name: str
    email: str
    password: str

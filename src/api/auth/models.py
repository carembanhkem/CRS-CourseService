from enum import Enum
from sqlmodel import Field, SQLModel
from typing import Optional


class UserType(str, Enum):
    INSTRUCTOR = "INSTRUCTOR"
    PLAYER = "PLAYER"


class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    name: str
    email: str
    cognito_sub: str

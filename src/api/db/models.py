from datetime import datetime
from enum import Enum
import uuid
from pydantic import BaseModel
from sqlmodel import Column, Field, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from api.courses.constant import CourseType


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
    courses: list["CourseModel"] = Relationship(  # this is a forward reference
        back_populates="instructor",
        sa_relationship_kwargs={"cascade": "all, delete", "lazy": "selectin"},
    )


class CourseModel(SQLModel, table=True):
    __tablename__ = "courses"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    description: Optional[str] = ""
    type: CourseType
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    created_at: datetime | None = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime | None = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    instructor: Optional[UserModel] = Relationship(back_populates="courses")

    def __repr__(self):
        return f"<Course {self.id}-{self.title}>"


class CourseTargetHero(SQLModel, table=True):
    __tablename__ = "course_target_hero"

    course_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False)
    )
    hero_id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False))

    def __repr__(self):
        return f"<CourseTargetHero {self.course_id}-{self.hero_id}>"


class Hero(SQLModel, table=True):
    __tablename__ = "heroes"

    id: int | None = Field(
        sa_column=Column(pg.INTEGER, nullable=False, primary_key=True)
    )
    name: str = Field(alias="localized_name")

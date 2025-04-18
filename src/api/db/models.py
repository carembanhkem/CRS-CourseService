from datetime import datetime
from enum import Enum
import uuid
from pydantic import BaseModel, ConfigDict
from sqlmodel import Column, Field, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from api import courses
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
    
    def __repr__(self):
        return f"<User {self.id}-{self.email}>"

    

class CourseTargetHero(SQLModel, table=True):
    __tablename__ = "course_target_hero"

    course_id: uuid.UUID = Field(
        default=None, primary_key=True, foreign_key="courses.id"
    )
    hero_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="heroes.id")

    def __repr__(self):
        return f"<CourseTargetHero {self.course_id}-{self.hero_id}>"

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
    heroes: list["Hero"] = Relationship(
        back_populates="courses",
        link_model=CourseTargetHero,
        sa_relationship_kwargs={"cascade": "all, delete", "lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Course {self.id}-{self.title}>"

class Hero(SQLModel, table=True):
    __tablename__ = "heroes"

    id: int | None = Field(
        sa_column=Column(pg.INTEGER, nullable=False, primary_key=True)
    )
    name: str = Field(alias="localized_name")
    courses: list[CourseModel] = Relationship(
        back_populates="heroes",
        link_model=CourseTargetHero,
        sa_relationship_kwargs={"cascade": "all, delete", "lazy": "selectin"},
    )
    def __repr__(self):
        return f"<Hero {self.id}-{self.name}>"

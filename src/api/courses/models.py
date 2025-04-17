from datetime import datetime
from enum import Enum
import uuid
from sqlmodel import Column, Field, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from typing import Optional

from api.auth import models
from api.db.models import user


class CourseType(str, Enum):
    ORDINARY = "ORDINARY"
    COACHING = "COACHING"


class LectureType(str, Enum):
    VIDEO = "VIDEO"
    TEXT = "TEXT"


class LectureSchema(SQLModel):
    id: int
    title: str
    description: Optional[str] = ""
    type: LectureType


class CourseModel(SQLModel, table=True):
    __tablename__ = "courses"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    description: Optional[str] = ""
    type: CourseType
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    created_at: datetime | None = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime | None = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    instructor: Optional[models.UserModel] = Relationship(back_populates="courses")

    def __repr__(self):
        return f"<Course {self.id}-{self.title}>"

class CourseTargetHero(SQLModel, table=True):
    __tablename__ = "course_target_hero"

    course_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False)
    )
    hero_id: int = Field(
        sa_column=Column(pg.INTEGER, primary_key=True, nullable=False)
    )

    def __repr__(self):
        return f"<CourseTargetHero {self.course_id}-{self.hero_id}>"

class CourseCreateSchema(SQLModel):
    title: str
    description: Optional[str] = ""
    type: CourseType
    target_heroes: list[int] = Field(default_factory=list)
    user_id: str


class CourseListSchema(SQLModel):
    results: list[CourseModel]
    count: int


class CourseDetailSchema(SQLModel):
    id: int
    title: str
    description: Optional[str] = ""
    type: CourseType
    lectures: list[LectureSchema]


class CourseUpdateSchema(SQLModel):
    title: str
    description: str

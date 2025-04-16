from enum import Enum

# from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional


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
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ""
    type: CourseType


class CourseCreateSchema(SQLModel):
    title: str
    description: Optional[str] = ""
    type: CourseType


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

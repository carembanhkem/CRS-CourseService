from datetime import datetime
from enum import Enum
import uuid
from pydantic import BaseModel, ConfigDict
from sqlmodel import Column, Field, Relationship, SQLModel
from typing import Optional
from api.heroes.schemas import HeroSchema

from api.courses.constants import CourseType

class CourseSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = ""
    type: CourseType
    user_id: uuid.UUID | None
    created_at: datetime | None
    updated_at: datetime | None
    heroes: list[HeroSchema] = []  # Forward reference to Hero model

    model_config = ConfigDict(from_attributes=True)


class CourseCreateSchema(BaseModel):
    title: str
    description: Optional[str] = ""
    type: CourseType
    heroes: list[int] = Field(default_factory=list)
    user_id: str


class CourseListSchema(BaseModel):
    results: list[CourseSchema]
    count: int


class CourseDetailSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    type: CourseType
    # lectures: list[LectureSchema]


class CourseUpdateSchema(BaseModel):
    title: str
    description: str

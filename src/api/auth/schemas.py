from enum import Enum
import uuid
from pydantic import BaseModel

from api.courses.schemas import CourseSchema


class UserSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    cognito_sub: str
    role: str
    courses: list[CourseSchema] = []  # List of courses associated with the user


class SignupRequestSchema(BaseModel):
    name: str
    email: str
    password: str

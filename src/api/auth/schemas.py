from enum import Enum
import uuid
from pydantic import BaseModel, ConfigDict, Field

from api.courses.schemas import CourseSchema


class UserSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    cognito_sub: str
    role: str
    # courses: list[CourseSchema] = Field(default_factory=list)


class UserToCourseSchema(UserSchema):
    courses: list[CourseSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SignupRequestSchema(BaseModel):
    name: str
    email: str
    password: str

class LoginRequestSchema(BaseModel):
    email: str
    password: str

class ConfirmSignupRequestSchema(BaseModel):
    email: str
    otp: str

class UserReadSchema(BaseModel):
    name: str
    email: str
    role: str
import os
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.courses.models import (
    CourseCreateSchema,
    CourseListSchema,
    CourseModel,
    CourseUpdateSchema,
)
from api.db.session import get_session
from .service import CourseService
from api.auth.models import UserModel
# from ..db.config import DATABASE_URL, AWS_REGION

course_router = APIRouter()
course_service = CourseService()


@course_router.get("/", response_model=CourseListSchema)
def read_courses(user_id: str, session: Session = Depends(get_session)) -> CourseListSchema:
    # print(os.environ.get("AWS_REGION"), AWS_REGION)
    # print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    results = course_service.get_courses(user_id,session)
    return {
        "results": results,
        "count": len(results)
    }


@course_router.post("/", response_model=CourseModel)
def create_course(
        payload: CourseCreateSchema, 
        session: Session = Depends(get_session)):
    data = payload.model_dump()
    new_course = course_service.create_course(data, session)
    return new_course


@course_router.get("/{course_id}")
def get_course(course_id: int) -> CourseModel:
    return CourseModel(
        id=course_id,
        title="How to play a support?",
        description="This is description",
        type="ORDINARY",
    )


@course_router.put("/{course_id}")
def update_course(course_id: int, payload: CourseUpdateSchema) -> CourseModel:
    data = payload.model_dump()
    return CourseModel(id=course_id, **data, type="ORDINARY")


@course_router.delete("/{course_id}")
def delete_course(course_id: int) -> dict:
    return {"result": "successful"}

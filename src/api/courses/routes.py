import os
from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.courses.models import (
    CourseCreateSchema,
    CourseListSchema,
    CourseModel,
    CourseUpdateSchema,
)
from api.db.session import get_session

course_router = APIRouter()
from ..db.config import DATABASE_URL, AWS_REGION


@course_router.get("/")
def read_courses() -> CourseListSchema:
    # print(os.environ.get("AWS_REGION"), AWS_REGION)
    # print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    return {
        "results": [
            CourseModel(
                id=1,
                title="How to play a support?",
                description="This is description",
                type="ORDINARY",
            ),
            CourseModel(
                id=2,
                title="How to play a carry?",
                description="This is description",
                type="COACHING",
            ),
        ],
        "count": 2,
    }  # type: ignore


@course_router.post("/", response_model=CourseModel)
def create_course(
        payload: CourseCreateSchema, 
        session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = CourseModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


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

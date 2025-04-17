import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.courses.models import (
    CourseCreateSchema,
    CourseListSchema,
    CourseModel,
    CourseUpdateSchema,
)
from api.db.session import get_session
from .service import CourseService
# from ..db.config import DATABASE_URL, AWS_REGION

course_router = APIRouter()
course_service = CourseService()


@course_router.get("/", response_model=CourseListSchema)
def read_courses(user_id: str, session: Session = Depends(get_session)):
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
    if not new_course:
        raise HTTPException(status_code=400, detail="Course creation failed")
    return new_course


@course_router.get("/{course_id}", response_model=CourseModel)
def get_course(course_id: str, session: Session = Depends(get_session)):
    result = course_service.get_course_by_id(course_id, session)
    if result is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return result


@course_router.put("/{course_id}", response_model=CourseModel)
def update_course(
    course_id: str, payload: CourseUpdateSchema, session: Session = Depends(get_session)
):
    data = payload.model_dump()
    return CourseModel(id=course_id, **data, type="ORDINARY")


@course_router.delete("/{course_id}")
def delete_course(course_id: int, session: Session = Depends(get_session)) -> dict:
    return {"result": "successful"}

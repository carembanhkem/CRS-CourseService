import uuid
from sqlmodel import Session, select
from .models import CourseModel


class CourseService:
    def create_course(self, data, session: Session):
        obj = CourseModel(**data)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def get_courses(self, user_id: str | None, session: Session):
        if not user_id:
            query = select(CourseModel).order_by(CourseModel.id.asc()).limit(10)
        else:
            query = (
                select(CourseModel)
                .where(CourseModel.user_id == user_id) # can compare string and uuid
                .order_by(CourseModel.id.asc())
                .limit(10)
            )
        results = session.exec(query).all()
        return results

    def get_course_by_id(self, course_id: str, session: Session):
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = session.exec(query).first()
        return result
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
                .where(
                    CourseModel.user_id
                    == "e4eaaaf2-d142-11e1-b3e4-080027620cdd"
                    )
                .order_by(CourseModel.id.asc())
                .limit(10)
            )
        results = session.exec(query).all()
        return results


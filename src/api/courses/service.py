import uuid
from sqlmodel import Session, select
from api.db.models import CourseModel, Hero


class CourseService:
    def create_course(self, data, session: Session):
        heroes = data.get("heroes", [])
        if not heroes:
            raise ValueError("Heroes list cannot be empty")
        target_heroes = []
        for hero_id in heroes:
            query = select(Hero).where(Hero.id == hero_id)
            result = session.exec(query).first()
            target_heroes.append(result)
        data["heroes"] = target_heroes
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
    
    def get_courses_target_heroes(self, hero_ids: list[str], session: Session):
        if not hero_ids:
            raise ValueError("Heroes list cannot be empty")
        query = select(CourseModel).join(CourseModel.heroes).where(Hero.id.in_(hero_ids))
        results = session.exec(query).all()
        return results

    def update_course(self, course_id: str, data, session: Session):
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = session.exec(query).first()
        if not result:
            return None
        for key, value in data.items():
            setattr(result, key, value)
        session.commit()
        session.refresh(result)
        return result

    def delete_course(self, course_id: str, session: Session):
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = session.exec(query).first()
        if not result:
            return False
        session.delete(result)
        session.commit()
        return True

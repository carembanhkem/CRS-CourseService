from sqlmodel import Session, select

from api.db.models import UserModel


class AuthService:

    def get_user(self, user_id, session: Session):
        query = select(UserModel).where(UserModel.id == user_id)
        result = session.exec(query).first()
        return result

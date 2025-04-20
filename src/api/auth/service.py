from sqlmodel import Session, select

from api.db.models import UserModel


class AuthService:
    def create_user(self, name: str, email: str, cognito_sub: str, session: Session):
        user = UserModel(
            name=name,
            email=email,
            cognito_sub=cognito_sub,
            role="instructor"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get_user(self, user_id, session: Session):
        query = select(UserModel).where(UserModel.id == user_id)
        result = session.exec(query).first()
        return result

    def get_user_by_email(self, email, session: Session):
        query = select(UserModel).where(UserModel.email == email)
        result = session.exec(query).first()
        return result

from api.auth.schemas import SignupRequestSchema, UserSchema
from api.auth.service import AuthService
from api.db.session import get_session
from api.helper.auth_helper import get_secret_hash
import boto3
from fastapi import APIRouter, Depends
from secret_keys import SecretKeys
from sqlalchemy.orm import Session


auth_router = APIRouter()
secret_keys = SecretKeys()
auth_service = AuthService()

AWS_COGNITO_CLIENT_ID = secret_keys.AWS_COGNITO_CLIENT_ID
AWS_COGNITO_CLIENT_SECRET = secret_keys.AWS_COGNITO_CLIENT_SECRET

cognito_client = boto3.client("cognito-idp", region_name=secret_keys.AWS_REGION)


@auth_router.post("/signup")
async def signup(data: SignupRequestSchema, db: Session = Depends(get_session)):
    secret_hash = get_secret_hash(
        data.email, AWS_COGNITO_CLIENT_ID, AWS_COGNITO_CLIENT_SECRET
    )

    cognito_response = cognito_client.sign_up(
        ClientId=AWS_COGNITO_CLIENT_ID,
        Username=data.email,
        Password=data.password,
        SecretHash=secret_hash,
        UserAttributes=[
            {"Name": "email", "Value": data.email},
            {"Name": "name", "Value": data.name},
        ],
    )

    return {"msg": "Signup successful. Please verify your email if required."}


@auth_router.get("/{user_id}", response_model=UserSchema)
async def get_me(user_id: str, session: Session = Depends(get_session)):
    user = auth_service.get_user(user_id, session)
    if not user:
        return {"msg": "User not found"}
    return user

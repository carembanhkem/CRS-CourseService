from api.auth.schemas import SignupRequestSchema, UserSchema, UserToCourseSchema
from api.auth.service import AuthService
from api.db.session import get_session
from api.helper.auth_helper import get_secret_hash
import boto3
from fastapi import APIRouter, Depends, Query
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

# get user by id with option with/without courses
@auth_router.get(
    "/{user_id}",
    response_model= UserToCourseSchema | UserSchema,  # Have to use union type to recognize when using UserToCourseSchema
    response_model_exclude_unset=True,
)
async def get_me(
    user_id: str,
    include_courses: bool = Query(
        False, description="Set to true to include user's courses"
    ),
    session: Session = Depends(get_session),
):
    user = auth_service.get_user(user_id, session)
    if not user:
        return {"msg": "User not found"}
    if not include_courses:
        user = UserSchema.model_validate(user, from_attributes=True)
    return user

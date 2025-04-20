from sqlmodel import Session
from api.auth.schemas import ConfirmSignupRequestSchema, LoginRequestSchema, SignupRequestSchema, UserSchema, UserToCourseSchema
from api.auth.service import AuthService
from api.db.middleware.auth_middleware import get_current_user
from api.db.session import get_session
from api.helper.auth_helper import get_secret_hash
import boto3
from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, Response
from secret_keys import SecretKeys


auth_router = APIRouter()
secret_keys = SecretKeys()
auth_service = AuthService()

AWS_COGNITO_CLIENT_ID = secret_keys.AWS_COGNITO_CLIENT_ID
AWS_COGNITO_CLIENT_SECRET = secret_keys.AWS_COGNITO_CLIENT_SECRET

cognito_client = boto3.client("cognito-idp", region_name=secret_keys.AWS_REGION)


@auth_router.post("/signup")
def signup(data: SignupRequestSchema, session: Session = Depends(get_session)):
    try:
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
        cognito_sub = cognito_response["UserSub"]
        if not cognito_sub:
            raise HTTPException(400, 'Cognito did not return a valid user sub')
    except Exception as ex:
        raise HTTPException(400, f"Cognito signup exception {ex}")

    new_user = auth_service.create_user(data.name, data.email, cognito_sub, session)

    return {"message": "Signup successful. Please verify your email if required."}


@auth_router.post("/login")
def login_user(data: LoginRequestSchema, response: Response):
    try:
        secret_hash = get_secret_hash(
            data.email, 
            AWS_COGNITO_CLIENT_ID, 
            AWS_COGNITO_CLIENT_SECRET
        )

        cognito_response = cognito_client.initiate_auth(
            ClientId=AWS_COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": data.email,
                "PASSWORD": data.password,
                "SECRET_HASH": secret_hash,
            },
        )

        auth_result = cognito_response.get("AuthenticationResult")

        if not auth_result:
            raise HTTPException(400, "Incorrect cognito response")

        access_token = auth_result.get("AccessToken")
        refresh_token = auth_result.get("RefreshToken")

        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
        response.set_cookie(
            key="refresh_token", value=refresh_token, httponly=True, secure=True
        )

        return {"message": "User logged in successfully."}
    except Exception as ex:
        raise HTTPException(400, f"Cognito signup exception {ex}")


@auth_router.post("/confirm-signup")
def confirm_signup(data: ConfirmSignupRequestSchema):
    try:
        secret_hash = get_secret_hash(
            data.email, AWS_COGNITO_CLIENT_ID, AWS_COGNITO_CLIENT_SECRET
        )

        cognito_response = cognito_client.confirm_sign_up(
            ClientId=AWS_COGNITO_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.otp,
            SecretHash=secret_hash
        )
        return {"message": "User confirmed successfully"}
    except Exception as ex:
        raise HTTPException(400, f"Cognito signup exception {ex}")


@auth_router.post("/refresh")
def refresh_token(
    refresh_token: str = Cookie(None),
    user_cognito_sub: str = Cookie(None),
    response: Response = None):
    try:
        secret_hash = get_secret_hash(
            user_cognito_sub, 
            AWS_COGNITO_CLIENT_ID, 
            AWS_COGNITO_CLIENT_SECRET
        )

        cognito_response = cognito_client.initiate_auth(
            ClientId=AWS_COGNITO_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
                'SECRET_HASH': secret_hash
            }
        )
        auth_result = cognito_response.get("AuthenticationResult")

        if not auth_result:
            raise HTTPException(400, "Incorrect cognito response")

        access_token = auth_result.get("AccessToken")

        response.set_cookie(
            key="access_token", value=access_token, httponly=True, secure=True
        )

        return {"message": "Access token refreshed!"}
    except Exception as ex:
        raise HTTPException(400, f"Cognito signup exception {ex}")


@auth_router.get("/me")
def protected_route(user =Depends(get_current_user)):
    return {"message": "You are authenticated!", "user": user}

# get user by id with option with/without courses
# @auth_router.get(
#     "/{user_id}",
#     response_model=UserToCourseSchema
#     | UserSchema,  # Have to use union type to recognize when using UserToCourseSchema
#     response_model_exclude_unset=True,
# )
# async def get_me(
#     user_id: str,
#     include_courses: bool = Query(
#         False, description="Set to true to include user's courses"
#     ),
#     session: Session = Depends(get_session),
# ):
#     user = auth_service.get_user(user_id, session)
#     if not user:
#         return {"msg": "User not found"}
#     if not include_courses:
#         user = UserSchema.model_validate(user, from_attributes=True)
#     return user

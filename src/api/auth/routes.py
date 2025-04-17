from api.db.session import get_session
from api.helper.auth_helper import get_secret_hash
import boto3
from re import S
from fastapi import APIRouter, Depends
from pydantic import Secret
from api.schemas.auth import SignupRequestSchema
from secret_keys import SecretKeys
from sqlalchemy.orm import Session


router = APIRouter()
secret_keys = SecretKeys()

AWS_COGNITO_CLIENT_ID = secret_keys.AWS_COGNITO_CLIENT_ID
AWS_COGNITO_CLIENT_SECRET = secret_keys.AWS_COGNITO_CLIENT_SECRET

cognito_client = boto3.client("cognito-idp", region_name=secret_keys.AWS_REGION)


@router.post("/signup")
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

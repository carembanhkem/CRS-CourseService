from json import load
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class SecretKeys(BaseSettings):
    AWS_COGNITO_CLIENT_ID: str = ""
    AWS_COGNITO_CLIENT_SECRET: str = ""
    AWS_REGION: str = ""
    DATABASE_URL: str = ""

    # model_config = {
    #     "env_file": ".env",
    #     "env_file_encoding": "utf-8",
    # }

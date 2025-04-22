from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class SecretKeys(BaseSettings):
    AWS_COGNITO_CLIENT_ID: str = ""
    AWS_COGNITO_CLIENT_SECRET: str = ""
    AWS_REGION: str = ""
    DATABASE_URL: str = ""
    AWS_RAW_VIDEOS_BUCKET: str = ""
    AWS_ACCESS_KEY_ID: str ="" # Docker can connect to AWS CLI setup so we need to set up. Or we must do some stuff in Dockerfile to set up AWS CLI properly
    AWS_SECRET_ACCESS_KEY: str =""

    # model_config = {
    #     "env_file": ".env",
    #     "env_file_encoding": "utf-8",
    # } # Khong dung duoc neu voi src chay uvicorn vi file .env o ngoai. load_env() hinh nhu load duoc tu ca ben ngoai nen moi chay duoc

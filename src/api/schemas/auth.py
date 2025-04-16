from pydantic import BaseModel

class SignupRequestSchema(BaseModel):
    name: str
    email: str
    password: str
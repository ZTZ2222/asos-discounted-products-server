from uuid import UUID
from pydantic import BaseModel, EmailStr, SecretStr


class UserRegister(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: SecretStr
    password_confirm: SecretStr


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    access_token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str

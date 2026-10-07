from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    email: EmailStr
    password: str


class UserResponse(BaseModel):

    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str
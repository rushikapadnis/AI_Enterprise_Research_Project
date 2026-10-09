from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.auth_service import create_access_token


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == user_data.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    user = User(
        email=user_data.email,
        password_hash=user_data.password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.email == login_data.email
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if user.password_hash != login_data.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user.id
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
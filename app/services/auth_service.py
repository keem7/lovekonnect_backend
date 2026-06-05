from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest
from app.schemas.user import UserCreate, UserResponse
from datetime import timedelta
from app.core.config import settings


def register_user(db: Session, user_data: RegisterRequest) -> User:
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Check if email exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        full_name=user_data.full_name,
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        gender=user_data.gender,
        date_of_birth=user_data.date_of_birth
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, login_data: LoginRequest) -> User:
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return user


def create_token(user: User) -> str:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    return access_token
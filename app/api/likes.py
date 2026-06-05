from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import oauth2_scheme, verify_token
from app.models.user import User
from app.models.like import Like
from app.schemas.like import LikeResponse
from app.services.match_service import check_and_create_match

router = APIRouter(prefix="/api/likes", tags=["Likes"])


def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    payload = verify_token(token)
    user_id = payload.get("user_id")
    return user_id


@router.post("/{user_id}", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def like_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Cannot like yourself
    if current_user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot like yourself"
        )

    # Check if user exists
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.sender_id == current_user_id,
        Like.receiver_id == user_id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked this user"
        )

    # Create like
    like = Like(sender_id=current_user_id, receiver_id=user_id)
    db.add(like)
    db.commit()
    db.refresh(like)

    # Check for mutual like and create match
    match = check_and_create_match(db, current_user_id, user_id)

    return like
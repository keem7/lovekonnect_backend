from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.core.database import get_db
from app.core.security import oauth2_scheme, verify_token
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import send_message, get_conversation, get_inbox
from app.services.match_service import is_matched

router = APIRouter(prefix="/api/messages", tags=["Messages"])


def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    payload = verify_token(token)
    user_id = payload.get("user_id")
    return user_id


@router.post("/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message_endpoint(
    message_data: MessageCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Check if users are matched
    if not is_matched(db, user_id, message_data.receiver_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only message users you have matched with"
        )

    message = send_message(db, user_id, message_data.receiver_id, message_data.message)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not send message"
        )

    return message


@router.get("/conversation/{user_id}", response_model=List[MessageResponse])
def get_conversation_endpoint(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Check if users are matched
    if not is_matched(db, current_user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view conversations with matched users"
        )

    messages = get_conversation(db, current_user_id, user_id)
    return messages


@router.get("/inbox")
def get_inbox_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    inbox = get_inbox(db, user_id)
    return inbox
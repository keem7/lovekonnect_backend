from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.core.database import get_db
from app.core.security import oauth2_scheme, verify_token
from app.models.match import Match
from app.schemas.match import MatchResponse
from app.services.match_service import get_user_matches, is_matched

router = APIRouter(prefix="/api/matches", tags=["Matches"])


def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    payload = verify_token(token)
    user_id = payload.get("user_id")
    return user_id


@router.get("", response_model=List[Dict])
def get_matches(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    matches = get_user_matches(db, user_id)
    return matches


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    # Verify user is part of this match
    if match.user1_id != user_id and match.user2_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this match"
        )

    return match
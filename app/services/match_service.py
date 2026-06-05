from sqlalchemy.orm import Session

from app.models.like import Like
from app.models.match import Match
from app.models.user import User


def check_and_create_match(db: Session, sender_id: int, receiver_id: int) -> Match | None:
    # Check if receiver already liked sender (mutual like)
    existing_like = db.query(Like).filter(
        Like.sender_id == receiver_id,
        Like.receiver_id == sender_id
    ).first()

    if existing_like:
        # Create a match
        # Determine smaller user ID as user1
        user1_id = min(sender_id, receiver_id)
        user2_id = max(sender_id, receiver_id)

        # Check if match already exists
        existing_match = db.query(Match).filter(
            Match.user1_id == user1_id,
            Match.user2_id == user2_id
        ).first()

        if not existing_match:
            new_match = Match(user1_id=user1_id, user2_id=user2_id)
            db.add(new_match)
            db.commit()
            db.refresh(new_match)
            return new_match
        return existing_match

    return None


def get_user_matches(db: Session, user_id: int):
    matches = db.query(Match).filter(
        (Match.user1_id == user_id) | (Match.user2_id == user_id)
    ).all()

    result = []
    for match in matches:
        other_user_id = match.user2_id if match.user1_id == user_id else match.user1_id
        other_user = db.query(User).filter(User.id == other_user_id).first()
        if other_user:
            result.append({
                "match": match,
                "user": other_user
            })

    return result


def is_matched(db: Session, user1_id: int, user2_id: int) -> bool:
    match = db.query(Match).filter(
        ((Match.user1_id == user1_id) & (Match.user2_id == user2_id)) |
        ((Match.user1_id == user2_id) & (Match.user2_id == user1_id))
    ).first()
    return match is not None
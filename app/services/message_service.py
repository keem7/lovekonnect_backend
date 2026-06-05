from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.match import Match


def send_message(db: Session, sender_id: int, receiver_id: int, message_text: str) -> Message:
    # Check if users are matched
    match = db.query(Match).filter(
        ((Match.user1_id == sender_id) & (Match.user2_id == receiver_id)) |
        ((Match.user1_id == receiver_id) & (Match.user2_id == sender_id))
    ).first()

    if not match:
        return None

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=message_text
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_conversation(db: Session, user1_id: int, user2_id: int):
    messages = db.query(Message).filter(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
        ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    ).order_by(Message.created_at).all()

    return messages


def get_inbox(db: Session, user_id: int):
    # Get all conversations where user is either sender or receiver
    messages = db.query(Message).filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.created_at.desc()).all()

    # Group by conversation partner
    conversations = {}
    for message in messages:
        partner_id = message.receiver_id if message.sender_id == user_id else message.sender_id
        if partner_id not in conversations:
            conversations[partner_id] = []
        conversations[partner_id].append(message)

    return conversations
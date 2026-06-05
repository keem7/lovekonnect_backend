from pydantic import BaseModel
from datetime import datetime


class LikeCreate(BaseModel):
    receiver_id: int


class LikeResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    created_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import datetime


class MatchResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    matched_at: datetime

    class Config:
        from_attributes = True
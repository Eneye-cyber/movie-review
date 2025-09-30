from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RatingBase(BaseModel):
    rating: int
    review: Optional[str] = None

class RatingCreate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class RatingListResponse(BaseModel):
    ratings: list[RatingResponse]
    total: int
    page: int
    limit: int
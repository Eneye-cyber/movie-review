from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import html

class RatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(None, max_length=2000)

    @validator('review')
    def sanitize_review(cls, v):
        """Sanitize review text"""
        if v is None:
            return v
        # Remove excessive whitespace and sanitize HTML
        v = ' '.join(v.split())
        return html.escape(v)

class RatingCreate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    username: str

    class Config:
        from_attributes = True

class RatingListResponse(BaseModel):
    ratings: list[RatingResponse]
    total: int
    page: int
    limit: int
    total_pages: int
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MovieBase(BaseModel):
    title: str
    genre: str
    release_year: int
    description: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    created_by: int
    created_at: datetime
    ratings_count: int
    ratings_avg: float

    class Config:
        from_attributes = True

class MovieListResponse(BaseModel):
    movies: list[MovieResponse]
    total: int
    page: int
    limit: int
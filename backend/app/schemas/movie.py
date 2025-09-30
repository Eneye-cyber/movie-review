from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import html

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    genre: str = Field(..., min_length=1, max_length=50)
    release_year: int = Field(..., ge=1888, le=datetime.now().year + 5)  # First movie was 1888
    description: Optional[str] = Field(None, max_length=1000)

    @validator('title', 'genre', 'description')
    def sanitize_text(cls, v):
        """Basic HTML sanitization to prevent XSS"""
        if v is None:
            return v
        return html.escape(v)

    @validator('genre')
    def validate_genre(cls, v):
        """Validate common movie genres"""
        common_genres = [
            'action', 'adventure', 'animation', 'comedy', 'crime', 'documentary',
            'drama', 'fantasy', 'historical', 'horror', 'mystery', 'romance',
            'sci-fi', 'thriller', 'western', 'biography', 'musical', 'family',
            'war', 'sports', 'superhero', 'noir'
        ]
        
        # Allow custom genres but validate format
        if not re.match("^[a-zA-Z\\-\\s]+$", v):
            raise ValueError('Genre can only contain letters, spaces, and hyphens')
        
        # Convert to lowercase for comparison
        v_lower = v.lower().strip()
        
        # Check if it's a common genre or contains common genre words
        is_valid = any(
            common_genre in v_lower or v_lower in common_genre 
            for common_genre in common_genres
        )
        
        if not is_valid and len(v_lower) < 3:
            raise ValueError('Genre seems invalid. Please use common movie genres')
            
        return v.title()  # Standardize capitalization

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
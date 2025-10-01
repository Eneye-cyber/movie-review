from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
import re
import math

from app.database import get_db
from app.schemas.movie import MovieCreate, MovieResponse, MovieListResponse
from app.schemas.rating import RatingCreate, RatingResponse, RatingListResponse
from app.crud.movie import get_movies, get_movie_by_id, create_movie, delete_movie
from app.crud.rating import create_or_update_rating, get_ratings_by_movie, update_movie_ratings_stats
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/movies", tags=["movies"])

def sanitize_search_query(search: str) -> str:
    """Sanitize search query to prevent injection attacks"""
    if not search:
        return ""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[;\"\']', '', search)
    return sanitized.strip()

@router.post("/", response_model=MovieResponse)
def add_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a new movie with validation
    """
    # Additional server-side validation
    if len(movie.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie title cannot be empty"
        )
    
    return create_movie(db=db, movie=movie, user_id=current_user.id)

@router.get("/", response_model=MovieListResponse)
def list_movies(
    genre: str = Query(None, description="Filter by genre", max_length=50),
    min_year: int = Query(None, description="Minimum release year", ge=1888, le=2100),
    max_year: int = Query(None, description="Maximum release year", ge=1888, le=2100),
    search: str = Query(None, description="Search in title or description", max_length=100),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    List movies with comprehensive input validation
    """
    # Validate year range
    if min_year and max_year and min_year > max_year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_year cannot be greater than max_year"
        )
    
    # Sanitize search query
    sanitized_search = sanitize_search_query(search) if search else None
    
    skip = (page - 1) * limit
    result = get_movies(
        db=db,
        skip=skip,
        limit=limit,
        genre=genre,
        min_year=min_year,
        max_year=max_year,
        search=sanitized_search
    )
    total_pages = math.ceil(result["total"] / result["limit"]) if result["limit"] else 1
    return MovieListResponse(
        movies=result["movies"],
        total=result["total"],
        page=result["page"],
        limit=result["limit"],
        total_pages=total_pages
    )

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int = Path(..., ge=1, description="Movie ID"), db: Session = Depends(get_db)):
    """
    Get movie details with ID validation
    """
    movie = get_movie_by_id(db, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie

@router.post("/{movie_id}/ratings", response_model=RatingResponse)
def add_rating(
    movie_id: int = Path(..., ge=1, description="Movie ID"),
    rating: RatingCreate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add or update rating with comprehensive validation
    """
    # Check if movie exists
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    # Prevent self-rating if user created the movie (optional business rule)
    # if movie.created_by == current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="You cannot rate your own movie"
    #     )
    
    # Create or update rating
    new_rating = create_or_update_rating(
        db=db,
        rating=rating,
        movie_id=movie_id,
        user_id=current_user.id
    )
    
    # Update movie rating statistics
    update_movie_ratings_stats(db, movie_id)
    
    return new_rating

@router.get("/{movie_id}/ratings", response_model=RatingListResponse)
def get_movie_ratings(
    movie_id: int = Path(..., ge=1, description="Movie ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get paginated ratings for a movie
    """
    # Verify movie exists
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    skip = (page - 1) * limit
    result = get_ratings_by_movie(db, movie_id=movie_id, skip=skip, limit=limit)
    total_pages = math.ceil(result["total"] / result["limit"]) if result["limit"] else 1

    return RatingListResponse(
        ratings=result["ratings"],
        total=result["total"],
        page=result["page"],
        limit=result["limit"],
        total_pages=total_pages

    )

@router.delete("/{movie_id}")
def delete_movie_endpoint(
    movie_id: int = Path(..., ge=1, description="Movie ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a movie with ownership validation
    """
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    # Only allow the creator to delete the movie
    if movie.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this movie"
        )
    
    delete_movie(db, movie_id)
    return {"message": "Movie deleted successfully"}
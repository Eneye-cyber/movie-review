from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.movie import MovieCreate, MovieResponse, MovieListResponse
from app.schemas.rating import RatingCreate, RatingResponse, RatingListResponse
from app.crud.movie import get_movies, get_movie_by_id, create_movie, delete_movie
from app.crud.rating import create_or_update_rating, get_ratings_by_movie, update_movie_ratings_stats
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.post("/", response_model=MovieResponse)
def add_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_movie(db=db, movie=movie, user_id=current_user.id)

@router.get("/", response_model=MovieListResponse)
def list_movies(
    genre: str = Query(None, description="Filter by genre"),
    min_year: int = Query(None, description="Minimum release year"),
    max_year: int = Query(None, description="Maximum release year"),
    search: str = Query(None, description="Search in title or description"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    result = get_movies(
        db=db,
        skip=skip,
        limit=limit,
        genre=genre,
        min_year=min_year,
        max_year=max_year,
        search=search
    )
    return MovieListResponse(
        movies=result["movies"],
        total=result["total"],
        page=result["page"],
        limit=result["limit"]
    )

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = get_movie_by_id(db, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie

@router.post("/{movie_id}/ratings", response_model=RatingResponse)
def add_rating(
    movie_id: int,
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if movie exists
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    # Validate rating range
    if not (1 <= rating.rating <= 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
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
    movie_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    result = get_ratings_by_movie(db, movie_id=movie_id, skip=skip, limit=limit)
    return RatingListResponse(
        ratings=result["ratings"],
        total=result["total"],
        page=result["page"],
        limit=result["limit"]
    )

@router.delete("/{movie_id}")
def delete_movie_endpoint(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
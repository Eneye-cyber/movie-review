from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.rating import Rating
from app.models.movie import Movie
from app.schemas.rating import RatingCreate

def get_rating_by_user_and_movie(db: Session, user_id: int, movie_id: int):
    return db.query(Rating).filter(
        Rating.user_id == user_id,
        Rating.movie_id == movie_id
    ).first()

def create_or_update_rating(db: Session, rating: RatingCreate, movie_id: int, user_id: int):
    # Check if rating exists
    existing_rating = get_rating_by_user_and_movie(db, user_id, movie_id)
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating.rating
        existing_rating.review = rating.review
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Create new rating
        db_rating = Rating(**rating.dict(), movie_id=movie_id, user_id=user_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

def get_ratings_by_movie(db: Session, movie_id: int, skip: int = 0, limit: int = 100):
    query = db.query(Rating).filter(Rating.movie_id == movie_id)
    total = query.count()
    ratings = query.offset(skip).limit(limit).all()
    
    return {
        "ratings": ratings,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit
    }

def get_ratings_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    query = db.query(Rating).filter(Rating.user_id == user_id)
    total = query.count()
    ratings = query.offset(skip).limit(limit).all()
    
    return {
        "ratings": ratings,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit
    }

def update_movie_ratings_stats(db: Session, movie_id: int):
    """Update aggregated rating statistics for a movie"""
    from sqlalchemy import func
    
    stats = db.query(
        func.count(Rating.id).label('count'),
        func.avg(Rating.rating).label('avg')
    ).filter(Rating.movie_id == movie_id).first()
    
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        movie.ratings_count = stats.count or 0
        movie.ratings_avg = float(stats.avg or 0.0)
        db.commit()
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.movie import Movie
from app.schemas.movie import MovieCreate

def get_movies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    genre: str = None,
    min_year: int = None,
    max_year: int = None,
    search: str = None
):
    query = db.query(Movie)
    
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    
    if min_year:
        query = query.filter(Movie.release_year >= min_year)
    
    if max_year:
        query = query.filter(Movie.release_year <= max_year)
    
    if search:
        query = query.filter(
            or_(
                Movie.title.ilike(f"%{search}%"),
                Movie.description.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    movies = query.offset(skip).limit(limit).all()
    
    return {
        "movies": movies,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit
    }

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.id == movie_id).first()

def create_movie(db: Session, movie: MovieCreate, user_id: int):
    db_movie = Movie(**movie.model_dump(), created_by=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        db.delete(movie)
        db.commit()
    return movie
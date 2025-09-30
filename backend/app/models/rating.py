from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
    
    # Ensure unique rating per user per movie
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

# Add unique constraint separately to avoid issues with __table_args__
from sqlalchemy import UniqueConstraint
Rating.__table_args__ += (UniqueConstraint('movie_id', 'user_id', name='unique_user_movie_rating'),)
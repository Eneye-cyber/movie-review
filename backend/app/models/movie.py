from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=False)
    release_year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Aggregated fields for performance
    ratings_count = Column(Integer, default=0)
    ratings_avg = Column(Float, default=0.0)
    
    # Relationships
    creator = relationship("User", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie")
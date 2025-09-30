from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.rating import RatingListResponse
from app.crud.rating import get_ratings_by_user
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["ratings"])

@router.get("/{user_id}/ratings", response_model=RatingListResponse)
def get_user_ratings(
    user_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Users can only view their own ratings
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these ratings"
        )
    
    skip = (page - 1) * limit
    result = get_ratings_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return RatingListResponse(
        ratings=result["ratings"],
        total=result["total"],
        page=result["page"],
        limit=result["limit"]
    )
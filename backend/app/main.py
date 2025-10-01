from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.database import engine, Base
from app.models import user, movie, rating
from app.api.endpoints import auth, movies, ratings

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create tables
user.Base.metadata.create_all(bind=engine)
movie.Base.metadata.create_all(bind=engine)
rating.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Rating Platform",
    description="A platform for users to add and rate movies",
    version="1.0.0"
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Custom validation error handler"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error['loc'])
        errors.append({
            "field": field,
            "message": error['msg'],
            "type": error['type']
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_type": "http_error"
        }
    )
    
# Include routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(ratings.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Rating Platform"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "postgresql" if os.getenv("USE_SQLITE", "false").lower() == "false" else "sqlite"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
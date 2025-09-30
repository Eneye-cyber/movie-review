from fastapi import FastAPI
from app.database import engine
from app.models import user, movie, rating
from app.api.endpoints import auth, movies, ratings

# Create tables
user.Base.metadata.create_all(bind=engine)
movie.Base.metadata.create_all(bind=engine)
rating.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Rating Platform",
    description="A platform for users to add and rate movies",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(ratings.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Rating Platform"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
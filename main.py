from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Movie, Base
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Ensure tables are created in the database at startup
Base.metadata.create_all(bind=engine)

# Pydantic models for request/response
class MovieCreate(BaseModel):
    title: str
    director: str
    year: int

class MovieOut(MovieCreate):
    id: int

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/movies/", response_model=MovieOut)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=List[MovieOut])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API powered by PostgreSQL!"}

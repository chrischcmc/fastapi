from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Movie, Base
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import List

app = FastAPI()
Base.metadata.create_all(bind=engine)

class MovieCreate(BaseModel):
    title: str
    director: str
    year: int

class MovieOut(MovieCreate):
    id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory "database"
movies_db = []

# Request/Response models
class Movie(BaseModel):
    id: int
    title: str
    director: str
    year: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API!"}

@app.post("/movies/", response_model=Movie)
def add_movie(movie: Movie):
    # Check if movie already exists
    for m in movies_db:
        if m.id == movie.id:
            raise HTTPException(status_code=400, detail="Movie already exists")
    movies_db.append(movie)
    return movie

@app.get("/movies/", response_model=List[Movie])
def list_movies():
    return movies_db

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")
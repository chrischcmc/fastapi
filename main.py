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

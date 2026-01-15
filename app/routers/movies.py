from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models import Movie, UserMovie
from app.schemas import AddWatchedMovie

router = APIRouter()

@router.post("/movies/watched")
async def add_watched_movie(
    movie_data: AddWatchedMovie,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user["sub"])
    
    # TODO: implement logic
    # 1. Check if movie exists in movies table
    # 2. If not, return error (we'll fix this later with TMDB API)
    # 3. Check if user already watched this movie
    # 4. Create UserMovie entry
    # 5. Return response
    movie = db.query(Movie).filter(Movie.tmdb_id == movie_data.tmdb_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie does not exist in database.")

    existing_entry = db.query(UserMovie).filter(
        UserMovie.tmdb_id == movie_data.tmdb_id,
        UserMovie.user_id == user_id
        ).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail=f"movie entry already exists in {user_id} table")

    new_user_movie = UserMovie(
    user_id = user_id,
    tmdb_id = movie_data.tmdb_id,
    date_watched = movie_data.date_watched,
    user_rating = movie_data.user_rating
    )

    db.add(new_user_movie)
    db.commit()
    db.refresh(new_user_movie)

    return {"message": f"New Movie {movie_data.tmdb_id} addded to {user_id} table"}
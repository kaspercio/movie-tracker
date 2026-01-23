from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models import Movie, UserMovie, Review
from app.schemas import AddWatchedMovie, WatchedMovieResponse, AddReviewRequest

router = APIRouter()

@router.post("/movies/watched")
async def add_watched_movie(
    movie_data: AddWatchedMovie,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user["sub"])
    
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

@router.get("/movies/watched", response_model=list[WatchedMovieResponse])
async def get_watched_movies(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    user_id = int(current_user["sub"])
    
    results = db.query(UserMovie, Movie).join(
        Movie, UserMovie.tmdb_id == Movie.tmdb_id
    ).filter(UserMovie.user_id == user_id).all()

    return [
        {
        "tmdb_id": user_movie.tmdb_id,
        "title": movie.title,
        "year": movie.year,
        "poster_url": movie.poster_url,
        "vote_average": movie.vote_average,
        "date_watched": user_movie.date_watched,
        "user_rating": user_movie.user_rating
    }
    for user_movie, movie in results
    ]
    
@router.post("/movies/{tmdb_id}/review")
async def add_review(
    tmdb_id: int,  # From URL path
    review_data: AddReviewRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user["sub"])
    
    # check if movie exists
    movie = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie does not exist in database.")
    # check if user already reviewed this movie (unique constraint)
    movie_review = db.query(Review).filter(
        Review.tmdb_id == tmdb_id,
        Review.user_id == user_id
    ).first()
    if movie_review:
        raise HTTPException(status_code=400, detail="Movie has been reviewed already.")
    # create Review entry
    new_movie_review = Review(
    user_id = user_id,
    tmdb_id = tmdb_id,
    review_text = review_data.review_text
    )

    db.add(new_movie_review)
    db.commit()
    db.refresh(new_movie_review)

    return {"message": f"New Movie {tmdb_id} added to user: {user_id} table"}
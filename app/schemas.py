from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional

# login endpoint schema
class LoginRequest(BaseModel):
    username: str
    password: str

# register endpoint schema
class RegisterRequest(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str

class AddWatchedMovie(BaseModel):
    tmdb_id: int
    date_watched: date
    user_rating: Optional[int] = None

    @field_validator('user_rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

class WatchedMovieResponse(BaseModel):
    tmdb_id: int
    title: str
    year: int
    poster_url: Optional[str]
    vote_average: Optional[float]
    date_watched: date
    user_rating: Optional[int]

class AddReviewRequest(BaseModel):
    review_text: str
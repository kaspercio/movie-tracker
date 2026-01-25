from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
from datetime import datetime

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

class UpdateWatchedMovie(BaseModel):
    date_watched: Optional[date] = None
    user_rating: Optional[int] = None
    
    @field_validator('user_rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

class UpdateReview(BaseModel):
    review_text: str

class ReviewResponse(BaseModel):
    review_id: int
    tmdb_id: int
    title: str  # from Movie
    year: Optional[int]  # from Movie
    poster_url: Optional[str]  # from Movie
    review_text: str
    created_at: datetime
    updated_at: Optional[datetime]
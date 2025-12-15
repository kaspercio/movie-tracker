from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import (
    DECIMAL, 
    String, 
    Text, 
    Date, 
    ForeignKey, 
    Integer, 
    CheckConstraint, 
    UniqueConstraint, 
    TIMESTAMP
)
from datetime import date, datetime
from app.database import Base
# model classes meaning the skeletons for the tables to be populated with data when tables are created.
class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	email: Mapped[str] = mapped_column(String(255), unique=True)
	hashed_password: Mapped[str] = mapped_column(String(255))
	username: Mapped[str] = mapped_column(String(30))
	created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

	def __repr__(self) -> str:
		return f"User(id={self.id!r}, email={self.email!r}, username={self.username!r})"
	
class Movie(Base):
	__tablename__ = "movies"

	tmdb_id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str] = mapped_column(String(255))
	year: Mapped[int]
	poster_url: Mapped[Optional[str]] = mapped_column(String(500))
	vote_average: Mapped[Optional[float]] = mapped_column(DECIMAL(3,1))
	overview: Mapped[Optional[str]] = mapped_column(Text)

	def __repr__(self) -> str:
		return ( 
			f"Movie(tmdb_id={self.tmdb_id!r}, title:{self.title!r}" 
			f"year:{self.year!r}, poster_url:{self.poster_url!r}" 
			f"vote_average:{self.vote_average!r}, overview{self.overview!r})"
		)

class UserMovie(Base):
	__tablename__ = "user_movies"

	entry_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	tmdb_id: Mapped[int] = mapped_column(ForeignKey("movies.tmdb_id"))
	date_watched: Mapped[date] = mapped_column(Date)
	user_rating: Mapped[Optional[int]] = mapped_column(
		Integer,
		CheckConstraint("user_rating >= 1 AND user_rating <= 5")
	)	
	__table_args__ = (
        UniqueConstraint('user_id', 'tmdb_id'),
    )

	def __repr__(self) -> str:
		return (
		f"UserMovie(entry_id={self.entry_id!r}, user_id={self.user_id!r}, "
		f"tmdb_id={self.tmdb_id!r}, date_watched={self.date_watched!r}, "
		f"user_rating={self.user_rating!r})"
	)

class Review(Base):
	__tablename__ = "reviews"

	review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	tmdb_id: Mapped[int] = mapped_column(ForeignKey("movies.tmdb_id"))
	review_text: Mapped[str] = mapped_column(Text)
	created_at: Mapped[datetime] = mapped_column(
		TIMESTAMP,
		server_default=func.now()
	)
	updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
	
	__table_args__ = (
		UniqueConstraint("user_id", "tmdb_id"),
	)

	def __repr__(self) -> str:
		return (
		f"Review(review_id={self.review_id!r}, user_id={self.user_id!r}, "
		f"tmdb_id={self.tmdb_id!r}, created_at={self.created_at!r}, "
		f"updated_at={self.updated_at!r})"
	)


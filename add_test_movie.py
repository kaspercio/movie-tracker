from app.database import SessionLocal
from app.models import Movie

db = SessionLocal()

# Create a test movie
test_movie = Movie(
    tmdb_id=12345,
    title="Test Movie",
    year=2024,
    poster_url="https://example.com/poster.jpg",
    vote_average=7.5,
    overview="A test movie for development"
)

db.add(test_movie)
db.commit()
db.refresh(test_movie)

print(f"Added movie: {test_movie.title} (tmdb_id: {test_movie.tmdb_id})")

db.close()
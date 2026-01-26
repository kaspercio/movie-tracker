# Movie Tracker API

A RESTful API for tracking movies you've watched and writing reviews, built with FastAPI, SQLAlchemy, and integrated with The Movie Database (TMDB) API.

## Features

- **User Authentication**: JWT-based registration and login
- **Movie Search**: Search for movies using TMDB API
- **Watched List Management**: Track movies with ratings and watch dates
- **Reviews**: Write, update, and delete movie reviews
- **Auto-population**: Automatically fetches movie metadata from TMDB

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (easily swappable for PostgreSQL/MySQL)
- **JWT**: Secure authentication
- **TMDB API**: Movie data integration
- **Pydantic**: Data validation

## Setup

### Prerequisites
- Python 3.10+
- TMDB API key ([get one here](https://www.themoviedb.org/settings/api))

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd movie-tracker
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file:
```
DATABASE_URL=sqlite:///./movie_tracker.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=3600
TMDB_API_KEY=your-tmdb-api-key
```

5. Create database tables
```bash
python create_tables.py
```

6. Run the server
```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /register` - Create new user account
- `POST /login` - Login and receive JWT token
- `GET /me` - Get current user info (protected)

### Movies
- `GET /movies/search?query={search}` - Search movies via TMDB
- `POST /movies/watched` - Add movie to watched list
- `GET /movies/watched` - Get all watched movies
- `PATCH /movies/watched/{tmdb_id}` - Update watched movie
- `DELETE /movies/watched/{tmdb_id}` - Remove from watched list

### Reviews
- `POST /movies/{tmdb_id}/review` - Add review for a movie
- `GET /reviews` - Get all your reviews
- `PATCH /movies/{tmdb_id}/review` - Update a review
- `DELETE /movies/{tmdb_id}/review` - Delete a review

## Example Usage

### Register
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com","password":"Pass123!","confirm_password":"Pass123!"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"Pass123!"}'
```

### Search Movies
```bash
curl "http://localhost:8000/movies/search?query=inception" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Add to Watched List
```bash
curl -X POST "http://localhost:8000/movies/watched" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tmdb_id":27205,"date_watched":"2025-01-15","user_rating":5}'
```

## Project Structure
```
movie-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── auth.py              # Authentication utilities
│   ├── database.py          # Database configuration
│   ├── dependencies.py      # FastAPI dependencies
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── routers/
│       ├── users.py         # User & auth endpoints
│       └── movies.py        # Movie & review endpoints
├── create_tables.py         # Database initialization
├── requirements.txt
├── .env
└── README.md
```

## Future Enhancements

- [ ] Watchlist (movies to watch)
- [ ] Movie recommendations
- [ ] User statistics (total watched, average rating)
- [ ] Filtering and sorting options
- [ ] Social features (follow users, share reviews)

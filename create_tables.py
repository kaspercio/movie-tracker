from app.database import engine, Base
from app.models import User, Movie, UserMovie, Review

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
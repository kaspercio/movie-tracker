from app.database import engine, Base
from app.models import User, Movie
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
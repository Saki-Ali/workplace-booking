from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Store the SQLite database file alongside the backend code inside the container
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""Database setup and session helpers.

This module configures the SQLAlchemy engine and session maker for the game. The
default configuration uses a local SQLite database file (`game.db`) stored in
the backend directory. SQLAlchemy’s declarative base is exposed as `Base` so
models can inherit from it.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL. Using a relative path stores the DB in the working
# directory. ``check_same_thread=False`` allows the connection to be shared
# across threads, which FastAPI uses when running in async mode.
SQLALCHEMY_DATABASE_URL = "sqlite:///./game.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI dependency that yields a database session and ensures it is
    properly closed after use. Usage:

    ```python
    from fastapi import Depends
    from .database import get_db

    @app.get("/players")
    def read_players(db: Session = Depends(get_db)):
        return db.query(models.Player).all()
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

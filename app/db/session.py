from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# Create database engine
# echo=True shows SQL queries in console (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Number of connections to keep open
    max_overflow=20  # Max connections beyond pool_size
)


# Create SessionLocal class
# Each instance is a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    Creates a new database session for each request
    Automatically closes session after request is done
    
    Usage in endpoints:
        def my_endpoint(db: Session = Depends(get_db)):
            # Use db here
            pass
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database
    Creates all tables defined in models
    Call this once when app starts
    """
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from collections.abc import Generator
from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session.
    This function is used as a dependency in FastAPI routes to provide a database session.
    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

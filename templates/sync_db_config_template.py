from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().database_url

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=get_settings().debug
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)


# Base class for declarative_base
class Base(DeclarativeBase):
    pass

# Create session generator for  session
 def get_session():
    """
    hronous generator function that returns a session.
    Create a new  session for each request and close it after the request is finished.

    Yields:
        session: A session object.

    Example Usage:
        ```
         with get_session() as session:
            # Do something with session
            pass
        ```
    """
    with SessionLocal() as session:
        yield session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().database_url

async_engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=get_settings().debug
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False
)


# Base class for declarative_base
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Create session generator for async session
async def get_async_session():
    """
    Asynchronous generator function that returns an async session.
    Create a new async session for each request and close it after the request is finished.

    Yields:
        async_session: An async session object.

    Example Usage:
        ```
        async with get_async_session() as async_session:
            # Do something with async session
            pass
        ```
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
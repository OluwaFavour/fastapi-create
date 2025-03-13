{% if is_async %}from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncAttrs,
){% else %}
from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.orm import sessionmaker{% endif %}
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().database_url

{% if is_async %}async_engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=get_settings().debug
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False
){% else %}
engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=get_settings().debug
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
){% endif %}



# Base class for declarative_base{% if is_async %}
class Base(AsyncAttrs, DeclarativeBase):{% else %}
class Base(DeclarativeBase):{% endif %}
    pass{% if is_async %}
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
        yield async_session{% else %}
# Create session generator for  session
def get_session():
    """
    Synchronous generator function that returns a session.
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
        yield session{% endif %}
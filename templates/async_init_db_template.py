from app.db.models import Base
from app.db.config import async_engine


async def init_db():
    """
    Initializes the database by creating all the tables defined in the metadata.

    Returns:
        None
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_db():
    """
    Dispose the database connection.

    This function is responsible for disposing the database connection by calling the `dispose()` method of the `async_engine` object.

    Parameters:
        None

    Returns:
        None
    """
    await async_engine.dispose()
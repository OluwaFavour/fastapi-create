from app.db.models import Base
from app.db.config import engine


def init_db():
    """
    Initializes the database by creating all the tables defined in the metadata.

    Returns:
        None
    """
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


def dispose_db():
    """
    Dispose the database connection.

    This function is responsible for disposing the database connection by calling the `dispose()` method of the `engine` object.

    Parameters:
        None

    Returns:
        None
    """
    engine.dispose()
from app.db.models import Base
from app.db.config import {% if is_async %}async_engine{% else %}engine{% endif %}


{% if is_async %}async {% endif %}def init_db():
    """
    Initializes the database by creating all the tables defined in the metadata.

    Returns:
        None
    """
    {% if is_async %}async with async_engine{% else %}engine{% endif %}.begin() as conn:
        {%if is_async%}await conn.run_sync(Base.metadata.create_all){% else %}Base.metadata.create_all(conn){% endif %}


{% if is_async %}async {% endif %}def dispose_db():
    """
    Dispose the database connection.

    This function is responsible for disposing the database connection by calling the `dispose()` method of the `async_engine` object.

    Parameters:
        None

    Returns:
        None
    """
    {% if is_async %}await async_engine{% else %}engine{% endif %}.dispose()
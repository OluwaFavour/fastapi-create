from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.init_db import init_db, dispose_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for managing the lifespan of the FastAPI application.

    Parameters:
    - app (FastAPI): The FastAPI application.

    Yields:
    None

    Usage:
    ```
    async with lifespan(app):
        # Code to be executed within the lifespan of the application
    ```
    """
    init_db()
    yield
    dispose_db()
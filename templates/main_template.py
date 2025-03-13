from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings
from app.lifespans import lifespan


app = FastAPI(
    debug=get_settings().debug,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    root_path="/api/v1",
)

# ADD MIDDLEWARES
## ADD SESSION MIDDLEWARE


## ADD CORS MIDDLEWARE



# ADD ROUTERS



@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
async def read_root(request: Request):
    base_url = request.base_url._url.rstrip("/")
    return {
        "message": "I'm alive!",
        "version": get_settings().app_version,
        "docs": {
            "redoc": f"{base_url}/api/redoc",
            "swagger": f"{base_url}/api/docs",
            "openapi": f"{base_url}/api/openapi.json",
        },
    }
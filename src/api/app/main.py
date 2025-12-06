from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import (
    movies_router,
    users_router,
    genres_router,
    directors_router,
    cast_router,
    ratings_router,
    recommendations_router,
)

# Database table creation should be performed by migrations (alembic).
# To keep backwards compatibility for simple local development you can enable
# automatic `create_all` by setting the `ENABLE_CREATE_ALL` environment
# variable to a truthy value (1/true/yes). By default this is disabled so
# the app does not perform schema changes on import (which can mask
# migration issues and cause startup ordering dependencies).
import os
import sys
if (
    os.environ.get("ENABLE_CREATE_ALL", "false").lower() in ("1", "true", "yes")
    and not os.environ.get("DOCS_MODE")
    and "pytest" not in sys.modules
):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Recommendation API",
    description="API for movie recommendation platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies_router)
app.include_router(users_router)
app.include_router(genres_router)
app.include_router(directors_router)
app.include_router(cast_router)
app.include_router(ratings_router)
app.include_router(recommendations_router)


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to Movie Recommendation API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


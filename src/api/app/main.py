from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import (
    movies_router,
    users_router,
    ratings_router,
    recommendations_router,
    genres_router,
)

# Database schema is managed by Alembic migrations.
# Run 'alembic upgrade head' before starting the application.

app = FastAPI(
    title="Movie Recommendation API",
    description="API for movie recommendation platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies_router)
app.include_router(users_router)
app.include_router(ratings_router)
app.include_router(recommendations_router)
app.include_router(genres_router)


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


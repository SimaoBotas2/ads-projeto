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

# Create database tables
import os
import sys
# Avoid DB initialization when generating docs (e.g., with pdoc) or running pytest
if not os.environ.get("DOCS_MODE") and "pytest" not in sys.modules:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Recommendation API",
    description="API for movie recommendation platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.app.database import Base, get_db
from api.app.routers import (
    movies_router,
    users_router,
    genres_router,
    directors_router,
    cast_router,
    ratings_router,
)


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency"""
    # Create FastAPI app for testing
    app = FastAPI(title="Movie Recommendation API - Test")
    
    # Include routers
    app.include_router(movies_router)
    app.include_router(users_router)
    app.include_router(genres_router)
    app.include_router(directors_router)
    app.include_router(cast_router)
    app.include_router(ratings_router)
    
    # Add root and health endpoints
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
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

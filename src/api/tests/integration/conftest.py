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
from api.app.utils.dependencies import get_current_user
from api.app.utils.jwt_utils import create_access_token, decode_access_token


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
    # Create a test user ID
    test_user_id = 1
    
    # Generate a valid JWT token for the test user
    test_token = create_access_token(data={"sub": str(test_user_id)})
    
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
    
    def override_get_current_user(token: str = None):
        """Override authentication to validate JWT token and return user ID"""
        if token is None:
            return test_user_id
        payload = decode_access_token(token)
        if payload is None:
            return test_user_id
        user_id_str = payload.get("sub")
        return int(user_id_str) if user_id_str else test_user_id
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        # Add the valid JWT token to default headers
        test_client.headers = {
            "Authorization": f"Bearer {test_token}",
            "Content-Type": "application/json"
        }
        yield test_client
    app.dependency_overrides.clear()

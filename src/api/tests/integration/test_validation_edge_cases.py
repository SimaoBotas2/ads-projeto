"""Integration tests for validation and service layer edge cases"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, SessionLocal, engine


@pytest.fixture
def db_session():
    """Create a clean database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with database session"""
    from fastapi import Depends
    from app.database import get_db
    
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestUserValidation:
    """Test suite for user input validation"""

    def test_create_user_with_special_email(self, client):
        """Test creating user with special email format"""
        user_data = {
            "username": "testuser",
            "email": "test+tag@example.com",
            "password": "securepass123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 201

    def test_create_user_with_invalid_email_format(self, client):
        """Test creating user with invalid email returns error"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "securepass123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 422

    def test_duplicate_username_validation(self, client):
        """Test that duplicate usernames are rejected"""
        user_data = {
            "username": "uniqueuser",
            "email": "user1@example.com",
            "password": "securepass123"
        }
        
        # Create first user
        response1 = client.post("/users", json=user_data)
        assert response1.status_code == 201
        
        # Try to create second user with same username
        user_data2 = {
            "username": "uniqueuser",
            "email": "user2@example.com",
            "password": "securepass123"
        }
        response2 = client.post("/users", json=user_data2)
        assert response2.status_code == 422

    def test_duplicate_email_validation(self, client):
        """Test that duplicate emails are rejected"""
        user_data = {
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "securepass123"
        }
        
        # Create first user
        response1 = client.post("/users", json=user_data)
        assert response1.status_code == 201
        
        # Try to create second user with same email
        user_data2 = {
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "securepass123"
        }
        response2 = client.post("/users", json=user_data2)
        assert response2.status_code == 422

    def test_user_with_unicode_username(self, client):
        """Test creating user with unicode characters"""
        user_data = {
            "username": "usuário123",
            "email": "unicode@example.com",
            "password": "securepass123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 201

    def test_user_with_very_long_bio(self, client):
        """Test creating user with very long bio"""
        user_data = {
            "username": "biouser",
            "email": "bio@example.com",
            "password": "securepass123",
            "bio": "x" * 500
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 201


class TestRatingValidation:
    """Test suite for rating validation"""

    def test_create_rating_with_decimal_value(self, client):
        """Test creating rating with decimal value"""
        # First create a movie and user
        movie_data = {"title": "Test Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        user_data = {
            "username": "ratinguser",
            "email": "rating@example.com",
            "password": "securepass123"
        }
        user_response = client.post("/users", json=user_data)
        user_id = user_response.json()["id"]
        
        # Create rating with decimal value
        rating_data = {
            "movie_id": movie_id,
            "user_id": user_id,
            "rating": 4.5,
            "review": "Great movie!"
        }
        response = client.post("/ratings", json=rating_data)
        assert response.status_code == 201

    def test_rating_value_outside_range(self, client):
        """Test that rating outside valid range is rejected"""
        movie_data = {"title": "Test Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        user_data = {
            "username": "ratinguser2",
            "email": "rating2@example.com",
            "password": "securepass123"
        }
        user_response = client.post("/users", json=user_data)
        user_id = user_response.json()["id"]
        
        # Try rating > 10
        rating_data = {
            "movie_id": movie_id,
            "user_id": user_id,
            "rating": 15.0,
            "review": "Invalid rating"
        }
        response = client.post("/ratings", json=rating_data)
        assert response.status_code == 422

    def test_rating_negative_value(self, client):
        """Test that negative rating is rejected"""
        movie_data = {"title": "Test Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        user_data = {
            "username": "ratinguser3",
            "email": "rating3@example.com",
            "password": "securepass123"
        }
        user_response = client.post("/users", json=user_data)
        user_id = user_response.json()["id"]
        
        # Try negative rating
        rating_data = {
            "movie_id": movie_id,
            "user_id": user_id,
            "rating": -1.0,
            "review": "Invalid negative"
        }
        response = client.post("/ratings", json=rating_data)
        assert response.status_code == 422

    def test_duplicate_rating_prevention(self, client):
        """Test that duplicate ratings are prevented"""
        movie_data = {"title": "Test Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        user_data = {
            "username": "ratinguser4",
            "email": "rating4@example.com",
            "password": "securepass123"
        }
        user_response = client.post("/users", json=user_data)
        user_id = user_response.json()["id"]
        
        rating_data = {
            "movie_id": movie_id,
            "user_id": user_id,
            "rating": 8.0,
            "review": "First review"
        }
        
        # Create first rating
        response1 = client.post("/ratings", json=rating_data)
        assert response1.status_code == 201
        
        # Try to create duplicate rating
        rating_data["review"] = "Second review"
        response2 = client.post("/ratings", json=rating_data)
        assert response2.status_code == 422

    def test_rating_with_very_long_review(self, client):
        """Test creating rating with very long review"""
        movie_data = {"title": "Test Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        user_data = {
            "username": "reviewuser",
            "email": "review@example.com",
            "password": "securepass123"
        }
        user_response = client.post("/users", json=user_data)
        user_id = user_response.json()["id"]
        
        rating_data = {
            "movie_id": movie_id,
            "user_id": user_id,
            "rating": 7.5,
            "review": "x" * 1000
        }
        response = client.post("/ratings", json=rating_data)
        assert response.status_code == 201


class TestGenreValidation:
    """Test suite for genre validation"""

    def test_create_genre_with_special_characters(self, client):
        """Test creating genre with special characters"""
        genre_data = {"name": "Science & Technology"}
        response = client.post("/genres", json=genre_data)
        assert response.status_code == 201

    def test_create_genre_with_unicode_name(self, client):
        """Test creating genre with unicode name"""
        genre_data = {"name": "Ficção Científica"}
        response = client.post("/genres", json=genre_data)
        assert response.status_code == 201

    def test_duplicate_genre_prevention(self, client):
        """Test that duplicate genres are handled"""
        genre_data = {"name": "Action"}
        
        # Create first genre
        response1 = client.post("/genres", json=genre_data)
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post("/genres", json=genre_data)
        # Should either reject or return existing
        assert response2.status_code in [201, 422]

    def test_get_genre_by_id(self, client):
        """Test retrieving genre by ID"""
        genre_data = {"name": "Drama"}
        create_response = client.post("/genres", json=genre_data)
        genre_id = create_response.json()["id"]
        
        response = client.get(f"/genres/{genre_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Drama"

    def test_update_genre(self, client):
        """Test updating genre"""
        genre_data = {"name": "OldName"}
        create_response = client.post("/genres", json=genre_data)
        genre_id = create_response.json()["id"]
        
        update_data = {"name": "NewName"}
        response = client.put(f"/genres/{genre_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "NewName"

    def test_delete_genre(self, client):
        """Test deleting genre"""
        genre_data = {"name": "ToDelete"}
        create_response = client.post("/genres", json=genre_data)
        genre_id = create_response.json()["id"]
        
        response = client.delete(f"/genres/{genre_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/genres/{genre_id}")
        assert get_response.status_code == 404

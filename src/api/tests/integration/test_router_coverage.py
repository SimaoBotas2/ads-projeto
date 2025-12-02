"""Integration tests for router endpoints - comprehensive coverage"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from api.app.main import app
from api.app.database import Base, SessionLocal, engine
from api.app.models.genre import Genre
from api.app.models.director import Director
from api.app.models.cast import Cast
from api.app.models.movie import Movie
from api.app.models.user import User
from api.app.models.rating import Rating


@pytest.fixture
def client():
    """Create test client"""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create database session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


class TestGenreRouterCoverage:
    """Test genre router endpoints for full coverage"""

    def test_get_genre_by_id(self, client, db_session):
        """Test getting genre by ID"""
        genre = Genre(name="Action")
        db_session.add(genre)
        db_session.commit()
        response = client.get(f"/genres/{genre.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Action"

    def test_get_genre_not_found(self, client):
        """Test getting non-existent genre"""
        response = client.get("/genres/99999")
        assert response.status_code == 404

    def test_update_genre(self, client, db_session):
        """Test updating genre"""
        genre = Genre(name="Old")
        db_session.add(genre)
        db_session.commit()
        response = client.put(f"/genres/{genre.id}", json={"name": "New"})
        assert response.status_code == 200
        assert response.json()["name"] == "New"

    def test_delete_genre(self, client, db_session):
        """Test deleting genre"""
        genre = Genre(name="ToDelete")
        db_session.add(genre)
        db_session.commit()
        response = client.delete(f"/genres/{genre.id}")
        assert response.status_code == 200

    def test_delete_genre_not_found(self, client):
        """Test deleting non-existent genre"""
        response = client.delete("/genres/99999")
        assert response.status_code == 404


class TestDirectorRouterCoverage:
    """Test director router endpoints for full coverage"""

    def test_get_director_by_id(self, client, db_session):
        """Test getting director by ID"""
        director = Director(name="Spielberg", birth_year=1946)
        db_session.add(director)
        db_session.commit()
        response = client.get(f"/directors/{director.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Spielberg"

    def test_get_director_not_found(self, client):
        """Test getting non-existent director"""
        response = client.get("/directors/99999")
        assert response.status_code == 404

    def test_update_director(self, client, db_session):
        """Test updating director"""
        director = Director(name="Old", birth_year=1950)
        db_session.add(director)
        db_session.commit()
        response = client.put(
            f"/directors/{director.id}",
            json={"name": "New", "birth_year": 1955}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New"

    def test_delete_director(self, client, db_session):
        """Test deleting director"""
        director = Director(name="ToDelete", birth_year=1960)
        db_session.add(director)
        db_session.commit()
        response = client.delete(f"/directors/{director.id}")
        assert response.status_code == 200

    def test_delete_director_not_found(self, client):
        """Test deleting non-existent director"""
        response = client.delete("/directors/99999")
        assert response.status_code == 404


class TestCastRouterCoverage:
    """Test cast router endpoints for full coverage"""

    def test_get_cast_by_id(self, client, db_session):
        """Test getting cast by ID"""
        cast = Cast(name="Actor", birth_year=1980)
        db_session.add(cast)
        db_session.commit()
        response = client.get(f"/cast/{cast.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Actor"

    def test_get_cast_not_found(self, client):
        """Test getting non-existent cast"""
        response = client.get("/cast/99999")
        assert response.status_code == 404

    def test_update_cast(self, client, db_session):
        """Test updating cast"""
        cast = Cast(name="OldName", birth_year=1980)
        db_session.add(cast)
        db_session.commit()
        response = client.put(f"/cast/{cast.id}", json={"name": "NewName"})
        assert response.status_code == 200
        assert response.json()["name"] == "NewName"

    def test_delete_cast(self, client, db_session):
        """Test deleting cast"""
        cast = Cast(name="ToDelete", birth_year=1985)
        db_session.add(cast)
        db_session.commit()
        response = client.delete(f"/cast/{cast.id}")
        assert response.status_code == 200

    def test_delete_cast_not_found(self, client):
        """Test deleting non-existent cast"""
        response = client.delete("/cast/99999")
        assert response.status_code == 404


class TestMovieRouterCoverage:
    """Test movie router endpoints for full coverage"""

    def test_get_movie_by_id(self, client, db_session):
        """Test getting movie by ID"""
        movie = Movie(title="TestMovie", release_date="2023-01-01")
        db_session.add(movie)
        db_session.commit()
        response = client.get(f"/movies/{movie.id}")
        assert response.status_code == 200
        assert response.json()["title"] == "TestMovie"

    def test_get_movie_not_found(self, client):
        """Test getting non-existent movie"""
        response = client.get("/movies/99999")
        assert response.status_code == 404

    def test_update_movie(self, client, db_session):
        """Test updating movie"""
        movie = Movie(title="Old", release_date="2023-01-01")
        db_session.add(movie)
        db_session.commit()
        response = client.put(f"/movies/{movie.id}", json={"title": "New"})
        assert response.status_code == 200
        assert response.json()["title"] == "New"

    def test_delete_movie(self, client, db_session):
        """Test deleting movie"""
        movie = Movie(title="ToDelete", release_date="2023-01-01")
        db_session.add(movie)
        db_session.commit()
        response = client.delete(f"/movies/{movie.id}")
        assert response.status_code == 200

    def test_delete_movie_not_found(self, client):
        """Test deleting non-existent movie"""
        response = client.delete("/movies/99999")
        assert response.status_code == 404

    def test_search_movies_empty(self, client):
        """Test searching movies when none exist"""
        response = client.get("/movies")
        assert response.status_code == 200
        assert response.json() == []


class TestUserRouterCoverage:
    """Test user router endpoints for full coverage"""

    def test_get_user_by_id(self, client, db_session):
        """Test getting user by ID"""
        user = User(username="user1", email="user1@example.com", password="pass")
        db_session.add(user)
        db_session.commit()
        response = client.get(f"/users/{user.id}")
        assert response.status_code == 200
        assert response.json()["username"] == "user1"

    def test_get_user_not_found(self, client):
        """Test getting non-existent user"""
        response = client.get("/users/99999")
        assert response.status_code == 404

    def test_update_user(self, client, db_session):
        """Test updating user"""
        user = User(username="user1", email="user1@example.com", password="pass")
        db_session.add(user)
        db_session.commit()
        response = client.put(
            f"/users/{user.id}",
            json={"email": "new@example.com"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "new@example.com"

    def test_delete_user(self, client, db_session):
        """Test deleting user"""
        user = User(username="delete", email="delete@example.com", password="pass")
        db_session.add(user)
        db_session.commit()
        response = client.delete(f"/users/{user.id}")
        assert response.status_code == 200

    def test_delete_user_not_found(self, client):
        """Test deleting non-existent user"""
        response = client.delete("/users/99999")
        assert response.status_code == 404


class TestRatingRouterCoverage:
    """Test rating router endpoints for full coverage"""

    def test_get_rating_by_id(self, client, db_session):
        """Test getting rating by ID"""
        user = User(username="user1", email="user1@example.com", password="pass")
        movie = Movie(title="Movie1", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        rating = Rating(user_id=user.id, movie_id=movie.id, evaluation=3)
        db_session.add(rating)
        db_session.commit()
        
        response = client.get(f"/ratings/{rating.id}")
        assert response.status_code == 200
        assert response.json()["evaluation"] == 3

    def test_get_rating_not_found(self, client):
        """Test getting non-existent rating"""
        response = client.get("/ratings/99999")
        assert response.status_code == 404

    def test_update_rating(self, client, db_session):
        """Test updating rating"""
        user = User(username="user2", email="user2@example.com", password="pass")
        movie = Movie(title="Movie2", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        rating = Rating(user_id=user.id, movie_id=movie.id, evaluation=2)
        db_session.add(rating)
        db_session.commit()
        
        response = client.put(f"/ratings/{rating.id}", json={"evaluation": 4})
        assert response.status_code == 200
        assert response.json()["evaluation"] == 4

    def test_delete_rating(self, client, db_session):
        """Test deleting rating"""
        user = User(username="user3", email="user3@example.com", password="pass")
        movie = Movie(title="Movie3", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        rating = Rating(user_id=user.id, movie_id=movie.id, evaluation=3)
        db_session.add(rating)
        db_session.commit()
        
        response = client.delete(f"/ratings/{rating.id}")
        assert response.status_code == 200

    def test_delete_rating_not_found(self, client):
        """Test deleting non-existent rating"""
        response = client.delete("/ratings/99999")
        assert response.status_code == 404

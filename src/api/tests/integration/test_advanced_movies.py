"""Integration tests for advanced movie operations"""
import pytest
from fastapi.testclient import TestClient
from api.app.main import app
from api.app.database import Base, SessionLocal, engine


class TestMovieAdvancedOperations:
    """Test suite for advanced movie operations"""

    def test_get_all_movies_empty_database(self, client):
        """Test getting all movies from empty database"""
        response = client.get("/movies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_movie_with_minimum_fields(self, client):
        """Test creating a movie with only minimum required fields"""
        movie_data = {
            "title": "Test Movie",
            "release_date": "2023-01-01"
        }
        response = client.post("/movies", json=movie_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Movie"
        assert "id" in data

    def test_create_movie_with_all_fields(self, client):
        """Test creating a movie with all fields"""
        movie_data = {
            "title": "Complete Movie",
            "description": "A complete movie with all fields",
            "release_date": "2023-06-15",
            "runtime": 120,
            "rating": 8.5
        }
        response = client.post("/movies", json=movie_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete Movie"
        assert data["runtime"] == 120
        assert data["rating"] == 8.5

    def test_get_movie_by_id(self, client):
        """Test retrieving a movie by ID"""
        # First create a movie
        movie_data = {"title": "Test Movie", "release_date": "2023-01-01"}
        create_response = client.post("/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/movies/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == movie_id
        assert data["title"] == "Test Movie"

    def test_get_nonexistent_movie_returns_404(self, client):
        """Test that getting nonexistent movie returns 404"""
        response = client.get("/movies/99999")
        assert response.status_code == 404

    def test_update_movie(self, client):
        """Test updating a movie"""
        # Create a movie
        movie_data = {"title": "Original Title", "release_date": "2023-01-01"}
        create_response = client.post("/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        # Update it
        update_data = {"title": "Updated Title", "description": "New description"}
        response = client.put(f"/movies/{movie_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    def test_delete_movie(self, client):
        """Test deleting a movie"""
        # Create a movie
        movie_data = {"title": "Delete Me", "release_date": "2023-01-01"}
        create_response = client.post("/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/movies/{movie_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/movies/{movie_id}")
        assert get_response.status_code == 404

    def test_search_movies_by_title(self, client):
        """Test searching movies by title"""
        # Create multiple movies
        movies = [
            {"title": "The Matrix", "release_date": "1999-03-31"},
            {"title": "The Matrix Reloaded", "release_date": "2003-05-15"},
            {"title": "Inception", "release_date": "2010-07-16"}
        ]
        
        for movie in movies:
            client.post("/movies", json=movie)
        
        # Search for Matrix movies
        response = client.get("/movies?search=Matrix")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_movie_validation_missing_title(self, client):
        """Test that creating movie without title fails"""
        movie_data = {"release_date": "2023-01-01"}
        response = client.post("/movies", json=movie_data)
        assert response.status_code == 422

    def test_movie_validation_missing_release_date(self, client):
        """Test that creating movie without release date fails"""
        movie_data = {"title": "Test Movie"}
        response = client.post("/movies", json=movie_data)
        assert response.status_code == 422

    def test_movie_with_special_characters_in_title(self, client):
        """Test creating movie with special characters"""
        movie_data = {
            "title": "Test & Movie: The Sequel (2023)",
            "release_date": "2023-01-01"
        }
        response = client.post("/movies", json=movie_data)
        assert response.status_code == 201

    def test_movie_with_very_long_description(self, client):
        """Test creating movie with very long description"""
        long_description = "a" * 1000
        movie_data = {
            "title": "Test Movie",
            "description": long_description,
            "release_date": "2023-01-01"
        }
        response = client.post("/movies", json=movie_data)
        assert response.status_code == 201


class TestMovieGenreAssociation:
    """Test suite for movie-genre association"""

    def test_movie_can_have_genres(self, client):
        """Test associating genres with a movie"""
        # First create a genre
        genre_data = {"name": "Sci-Fi"}
        genre_response = client.post("/genres", json=genre_data)
        genre_id = genre_response.json()["id"]
        
        # Create movie
        movie_data = {"title": "Space Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        # Associate genre with movie
        assoc_data = {"genre_id": genre_id}
        response = client.post(f"/movies/{movie_id}/genres", json=assoc_data)
        assert response.status_code in [200, 201]

    def test_filter_movies_by_genre(self, client):
        """Test filtering movies by genre"""
        # Create genre and movies
        genre_data = {"name": "Action"}
        genre_response = client.post("/genres", json=genre_data)
        genre_id = genre_response.json()["id"]
        
        movie_data = {"title": "Action Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        # Associate and filter
        client.post(f"/movies/{movie_id}/genres", json={"genre_id": genre_id})
        response = client.get(f"/genres/{genre_id}/movies")
        assert response.status_code == 200


class TestMovieDirectorAssociation:
    """Test suite for movie-director association"""

    def test_movie_can_have_directors(self, client):
        """Test associating directors with a movie"""
        # Create director
        director_data = {"name": "Steven Spielberg", "birth_year": 1946}
        director_response = client.post("/directors", json=director_data)
        director_id = director_response.json()["id"]
        
        # Create movie
        movie_data = {"title": "Director's Movie", "release_date": "2023-01-01"}
        movie_response = client.post("/movies", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        # Associate director with movie
        assoc_data = {"director_id": director_id}
        response = client.post(f"/movies/{movie_id}/directors", json=assoc_data)
        assert response.status_code in [200, 201]

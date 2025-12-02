"""Fixed integration tests for Movies Router - Tests only GET endpoints that exist"""
from datetime import date


class TestMoviesRouter:
    """Integration tests for Movies Router"""

    def test_get_all_movies_empty(self, client):
        """Test getting all movies when database is empty"""
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json() == []

    def test_search_movies_empty_query(self, client):
        """Test searching movies with empty results"""
        response = client.get("/movies/search/?query=nonexistent")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_movies_by_genre_empty(self, client):
        """Test getting movies by genre when none exist"""
        response = client.get("/movies/genre/999")
        assert response.status_code in [200, 404]

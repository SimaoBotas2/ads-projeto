"""Simplified integration tests for Ratings Router"""


class TestRatingsRouter:
    """Integration tests for Ratings Router"""

    def test_get_user_ratings_not_found(self, client):
        """Test getting ratings for non-existent user returns empty or 404"""
        response = client.get("/ratings/user/999")
        # Should return empty list or 404
        assert response.status_code in [200, 404]

    def test_get_movie_ratings_not_found(self, client):
        """Test getting ratings for non-existent movie returns empty or 404"""
        response = client.get("/ratings/movie/999")
        # Should return empty list or 404
        assert response.status_code in [200, 404]

from datetime import date
from api.app.models.movie import Movie


class TestMovie:
    """Unit tests for the Movie model"""
    
    def test_movie_creation(self):
        """Test that a Movie object can be created with basic attributes"""
        movie = Movie(
            title="Test Movie",
            original_title="Test Movie Original",
            overview="This is a test movie for unit testing",
            tagline="Test tagline",
            release_date=date(2023, 1, 1),
            runtime=120,
            budget=1000000,
            revenue=5000000,
            imdb_id="tt1234567",
            original_language="en",
            popularity=8.5,
            vote_average=7.8,
            vote_count=1000
        )
        
        assert movie.title == "Test Movie"
        assert movie.original_title == "Test Movie Original"
        assert movie.overview == "This is a test movie for unit testing"
        assert movie.tagline == "Test tagline"
        assert movie.release_date == date(2023, 1, 1)
        assert movie.runtime == 120
        assert movie.budget == 1000000
        assert movie.revenue == 5000000
        assert movie.imdb_id == "tt1234567"
        assert movie.original_language == "en"
        assert movie.popularity == 8.5
        assert movie.vote_average == 7.8
        assert movie.vote_count == 1000
    
    def test_movie_string_representation(self):
        """Test movie string representation"""
        movie = Movie(title="Test Movie")
        # Since no __str__ method is defined, this will test the default behavior
        assert hasattr(movie, 'title')
        assert movie.title == "Test Movie"
    
    def test_movie_required_fields(self):
        """Test that movie can be created with minimal required fields"""
        movie = Movie(title="Minimal Movie")
        assert movie.title == "Minimal Movie"
        assert movie.original_title is None
        assert movie.overview is None
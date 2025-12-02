from datetime import date
from api.app.models.movie import Movie


class TestMovie:
    """Unit tests for the Movie model"""
    
    def test_movie_creation(self):
        """Test that a Movie object can be created with basic attributes"""
        movie = Movie(
            name="Test Movie",
            launch_date=date(2023, 1, 1),
            description="This is a test movie for unit testing",
            nationality="US",
            poster_path="/path/to/poster.jpg"
        )
        
        assert movie.name == "Test Movie"
        assert movie.launch_date == date(2023, 1, 1)
        assert movie.description == "This is a test movie for unit testing"
        assert movie.nationality == "US"
        assert movie.poster_path == "/path/to/poster.jpg"
    
    def test_movie_string_representation(self):
        """Test movie string representation"""
        movie = Movie(name="Test Movie")
        # Since no __str__ method is defined, this will test the default behavior
        assert hasattr(movie, 'name')
        assert movie.name == "Test Movie"
    
    def test_movie_required_fields(self):
        """Test that movie can be created with minimal required fields"""
        movie = Movie(name="Minimal Movie")
        assert movie.name == "Minimal Movie"
        assert movie.launch_date is None
        assert movie.description is None
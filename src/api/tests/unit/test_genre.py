from api.app.models.genre import Genre


class TestGenre:
    """Unit tests for Genre Model"""
    
    def test_genre_creation(self):
        """Test that a Genre object can be created with all attributes"""
        genre = Genre(
            name="Action",
            description="Movies with action and adventure"
        )

        assert genre.name == "Action"
        assert genre.description == "Movies with action and adventure"

    def test_genre_required_fields(self):
        """Test that genre can be created with minimal required fields"""
        genre = Genre(name="Drama")

        assert genre.name == "Drama"
        assert genre.description is None

    def test_genre_with_special_characters(self):
        """Test genre creation with special characters in name"""
        genre = Genre(
            name="Science Fiction",
            description="Futuristic sci-fi movies"
        )

        assert genre.name == "Science Fiction"
        assert genre.description == "Futuristic sci-fi movies"

    def test_genre_with_empty_description(self):
        """Test genre creation with explicit empty description"""
        genre = Genre(name="Thriller", description="")

        assert genre.name == "Thriller"
        assert genre.description == ""

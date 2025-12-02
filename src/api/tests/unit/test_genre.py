from api.app.models.genre import Genre


class TestGenre:
    """Unit tests for Genre Model"""
    
    def test_genre_creation(self):
        """Test that a Genre object can be created with all attributes"""
        genre = Genre(name="Action")

        assert genre.name == "Action"

    def test_genre_required_fields(self):
        """Test that genre can be created with minimal required fields"""
        genre = Genre(name="Drama")

        assert genre.name == "Drama"

    def test_genre_with_special_characters(self):
        """Test genre creation with special characters in name"""
        genre = Genre(name="Science Fiction")

        assert genre.name == "Science Fiction"

    def test_genre_with_unicode_name(self):
        """Test genre creation with unicode characters"""
        genre = Genre(name="Fantaisie")

        assert genre.name == "Fantaisie"

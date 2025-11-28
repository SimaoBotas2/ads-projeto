from datetime import date
from api.app.models.director import Director


class TestDirector:
    """Unit tests for Director Model"""
    
    def test_director_creation(self):
        """Test that a Director object can be created with all attributes"""
        director = Director(
            name="Christopher Nolan",
            biography="Director of inception and dark knight",
            birth_date=date(1970, 7, 30),
            birth_place="London, England",
            profile_path="/path/to/image.jpg"
        )

        assert director.name == "Christopher Nolan"
        assert director.biography == "Director of inception and dark knight"
        assert director.birth_date == date(1970, 7, 30)
        assert director.birth_place == "London, England"
        assert director.profile_path == "/path/to/image.jpg"

    def test_director_required_fields(self):
        """Test that director can be created with minimal required fields"""
        director = Director(name="Test Director")

        assert director.name == "Test Director"
        assert director.biography is None
        assert director.birth_date is None
        assert director.birth_place is None
        assert director.profile_path is None

    def test_director_with_partial_fields(self):
        """Test director creation with some optional fields"""
        director = Director(
            name="Steven Spielberg",
            biography="Famous director",
            birth_date=date(1946, 12, 18)
        )

        assert director.name == "Steven Spielberg"
        assert director.biography == "Famous director"
        assert director.birth_date == date(1946, 12, 18)
        assert director.birth_place is None
        assert director.profile_path is None

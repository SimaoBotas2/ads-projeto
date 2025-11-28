from datetime import date
from api.app.models.cast import Cast


class TestCast:
    """Unit tests for Cast Model"""
    
    def test_cast_creation(self):
        """Test that a Cast object can be created with all attributes"""
        cast = Cast(
            name="Test Actor",
            biography="Actor born in test land",
            birth_date=date(1970, 1, 1),
            birth_place="Test Land"
        )

        assert cast.name == "Test Actor"
        assert cast.biography == "Actor born in test land"
        assert cast.birth_date == date(1970, 1, 1)
        assert cast.birth_place == "Test Land"

    def test_cast_required_fields(self):
        """Test that cast can be created with minimal required fields"""
        cast = Cast(name="Minimal Actor")

        assert cast.name == "Minimal Actor"
        assert cast.biography is None
        assert cast.birth_date is None
        assert cast.birth_place is None

    def test_cast_with_partial_fields(self):
        """Test cast creation with some optional fields"""
        cast = Cast(
            name="Keanu Reeves",
            biography="American actor",
            birth_date=date(1964, 9, 2)
        )

        assert cast.name == "Keanu Reeves"
        assert cast.biography == "American actor"
        assert cast.birth_date == date(1964, 9, 2)
        assert cast.birth_place is None
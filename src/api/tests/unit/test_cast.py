from api.app.models.cast import Cast


class TestCast:
    """Unit tests for Cast Model"""
    
    def test_cast_creation(self):
        """Test that a Cast object can be created with all attributes"""
        cast = Cast(
            name="Test Actor",
            nationality="American"
        )

        assert cast.name == "Test Actor"
        assert cast.nationality == "American"

    def test_cast_required_fields(self):
        """Test that cast can be created with minimal required fields"""
        cast = Cast(name="Minimal Actor")

        assert cast.name == "Minimal Actor"
        assert cast.nationality is None

    def test_cast_with_partial_fields(self):
        """Test cast creation with some optional fields"""
        cast = Cast(
            name="Keanu Reeves",
            nationality="American"
        )

        assert cast.name == "Keanu Reeves"
        assert cast.nationality == "American"
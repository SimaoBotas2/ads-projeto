from api.app.models.director import Director


class TestDirector:
    """Unit tests for Director Model"""
    
    def test_director_creation(self):
        """Test that a Director object can be created with all attributes"""
        director = Director(
            name="Christopher Nolan",
            nationality="British"
        )

        assert director.name == "Christopher Nolan"
        assert director.nationality == "British"

    def test_director_required_fields(self):
        """Test that director can be created with minimal required fields"""
        director = Director(name="Test Director")

        assert director.name == "Test Director"
        assert director.nationality is None

    def test_director_with_partial_fields(self):
        """Test director creation with some optional fields"""
        director = Director(
            name="Steven Spielberg",
            nationality="American"
        )

        assert director.name == "Steven Spielberg"
        assert director.nationality == "American"

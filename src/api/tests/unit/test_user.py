from api.app.models.user import User


class TestUser:
    """Unit tests for User Model"""
    
    def test_user_creation(self):
        """Test that a User object can be created with all attributes"""
        user = User(
            username="john_doe",
            email="john@example.com",
            password="hashed_password_123",
            name="John Doe"
        )

        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.password == "hashed_password_123"
        assert user.name == "John Doe"

    def test_user_required_fields(self):
        """Test that user can be created with minimal required fields"""
        user = User(
            username="jane_doe",
            email="jane@example.com",
            password="hashed_password_456"
        )

        assert user.username == "jane_doe"
        assert user.email == "jane@example.com"
        assert user.password == "hashed_password_456"
        assert user.name is None

    def test_user_with_special_characters(self):
        """Test user creation with special characters in email"""
        user = User(
            username="special_user",
            email="user+test@example.co.uk",
            password="hashed_pass"
        )

        assert user.username == "special_user"
        assert user.email == "user+test@example.co.uk"

    def test_user_with_long_name(self):
        """Test user creation with long name text"""
        long_name = "A" * 500
        user = User(
            username="name_user",
            email="name@example.com",
            password="hashed_pass",
            name=long_name
        )

        assert user.name == long_name
        assert len(user.name) == 500

    def test_user_timestamps_default_none(self):
        """Test that last_login is None before persistence"""
        user = User(
            username="timestamp_user",
            email="timestamp@example.com",
            password="hashed_pass"
        )

        # last_login should be None initially
        assert user.last_login is None

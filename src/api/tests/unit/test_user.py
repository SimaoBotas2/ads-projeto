from datetime import date, datetime
from api.app.models.user import User


class TestUser:
    """Unit tests for User Model"""
    
    def test_user_creation(self):
        """Test that a User object can be created with all attributes"""
        user = User(
            username="john_doe",
            email="john@example.com",
            hashed_password="hashed_password_123",
            full_name="John Doe",
            bio="Movie enthusiast"
        )

        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.full_name == "John Doe"
        assert user.bio == "Movie enthusiast"

    def test_user_required_fields(self):
        """Test that user can be created with minimal required fields"""
        user = User(
            username="jane_doe",
            email="jane@example.com",
            hashed_password="hashed_password_456"
        )

        assert user.username == "jane_doe"
        assert user.email == "jane@example.com"
        assert user.hashed_password == "hashed_password_456"
        assert user.full_name is None
        assert user.bio is None

    def test_user_with_special_characters(self):
        """Test user creation with special characters in email"""
        user = User(
            username="special_user",
            email="user+test@example.co.uk",
            hashed_password="hashed_pass"
        )

        assert user.username == "special_user"
        assert user.email == "user+test@example.co.uk"

    def test_user_with_long_bio(self):
        """Test user creation with long bio text"""
        long_bio = "A" * 500
        user = User(
            username="bio_user",
            email="bio@example.com",
            hashed_password="hashed_pass",
            bio=long_bio
        )

        assert user.bio == long_bio
        assert len(user.bio) == 500

    def test_user_timestamps_default_none(self):
        """Test that created_at and updated_at are None before persistence"""
        user = User(
            username="timestamp_user",
            email="timestamp@example.com",
            hashed_password="hashed_pass"
        )

        # These fields get their values from the database, not from Python
        assert not hasattr(user, 'created_at') or user.created_at is None
        assert not hasattr(user, 'updated_at') or user.updated_at is None

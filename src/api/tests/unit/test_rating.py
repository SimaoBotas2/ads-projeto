from datetime import date
from api.app.models.rating import Rating


class TestRating:
    """Unit tests for Rating Model"""
    
    def test_rating_creation(self):
        """Test that a Rating object can be created with all attributes"""
        rating = Rating(
            user_id=1,
            movie_id=1,
            rating=8.5,
            review="Great movie, highly recommend!"
        )

        assert rating.user_id == 1
        assert rating.movie_id == 1
        assert rating.rating == 8.5
        assert rating.review == "Great movie, highly recommend!"

    def test_rating_required_fields(self):
        """Test that rating can be created with minimal required fields"""
        rating = Rating(
            user_id=2,
            movie_id=2,
            rating=7.0
        )

        assert rating.user_id == 2
        assert rating.movie_id == 2
        assert rating.rating == 7.0
        assert rating.review is None

    def test_rating_with_min_value(self):
        """Test rating creation with minimum rating value"""
        rating = Rating(
            user_id=1,
            movie_id=3,
            rating=1.0,
            review="Terrible movie"
        )

        assert rating.rating == 1.0
        assert rating.review == "Terrible movie"

    def test_rating_with_max_value(self):
        """Test rating creation with maximum rating value"""
        rating = Rating(
            user_id=1,
            movie_id=4,
            rating=10.0,
            review="Perfect movie!"
        )

        assert rating.rating == 10.0

    def test_rating_with_decimal_values(self):
        """Test rating creation with decimal values"""
        rating = Rating(
            user_id=3,
            movie_id=5,
            rating=7.5
        )

        assert rating.rating == 7.5

    def test_rating_with_long_review(self):
        """Test rating creation with long review text"""
        long_review = "This is an excellent movie! " * 50
        rating = Rating(
            user_id=1,
            movie_id=6,
            rating=9.0,
            review=long_review
        )

        assert rating.review == long_review
        assert len(rating.review) > 1000

    def test_rating_timestamps_default_none(self):
        """Test that created_at and updated_at are None before persistence"""
        rating = Rating(
            user_id=4,
            movie_id=7,
            rating=6.5
        )

        # These fields get their values from the database, not from Python
        assert not hasattr(rating, 'created_at') or rating.created_at is None
        assert not hasattr(rating, 'updated_at') or rating.updated_at is None

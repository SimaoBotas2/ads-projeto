from api.app.models.rating import Rating


class TestRating:
    """Unit tests for Rating Model"""
    
    def test_rating_creation(self):
        """Test that a Rating object can be created with all attributes"""
        rating = Rating(
            user_id=1,
            movie_id=1,
            evaluation=3
        )

        assert rating.user_id == 1
        assert rating.movie_id == 1
        assert rating.evaluation == 3

    def test_rating_required_fields(self):
        """Test that rating can be created with minimal required fields"""
        rating = Rating(
            user_id=2,
            movie_id=2,
            evaluation=2
        )

        assert rating.user_id == 2
        assert rating.movie_id == 2
        assert rating.evaluation == 2

    def test_rating_with_min_value(self):
        """Test rating creation with minimum evaluation value"""
        rating = Rating(
            user_id=1,
            movie_id=3,
            evaluation=1
        )

        assert rating.evaluation == 1

    def test_rating_with_max_value(self):
        """Test rating creation with maximum evaluation value"""
        rating = Rating(
            user_id=1,
            movie_id=4,
            evaluation=4
        )

        assert rating.evaluation == 4

    def test_rating_with_different_values(self):
        """Test rating creation with different evaluation values"""
        rating = Rating(
            user_id=3,
            movie_id=5,
            evaluation=2
        )

        assert rating.evaluation == 2

    def test_rating_multiple_movies(self):
        """Test rating creation for multiple movies"""
        rating1 = Rating(user_id=1, movie_id=1, evaluation=1)
        rating2 = Rating(user_id=1, movie_id=2, evaluation=4)
        
        assert rating1.movie_id != rating2.movie_id
        assert rating1.evaluation != rating2.evaluation

    def test_rating_multiple_users(self):
        """Test rating creation by multiple users"""
        rating1 = Rating(user_id=1, movie_id=1, evaluation=1)
        rating2 = Rating(user_id=2, movie_id=1, evaluation=4)
        
        assert rating1.user_id != rating2.user_id
        assert rating1.evaluation != rating2.evaluation

"""Integration tests for service methods with additional coverage"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from api.app.main import app
from api.app.database import Base, SessionLocal, engine
from api.app.models.genre import Genre
from api.app.models.director import Director
from api.app.models.cast import Cast
from api.app.models.movie import Movie
from api.app.models.user import User
from api.app.models.rating import Rating
from api.app.services.genre_service import GenreService
from api.app.services.director_service import DirectorService
from api.app.services.cast_service import CastService
from api.app.services.movie_service import MovieService
from api.app.services.user_service import UserService
from api.app.services.rating_service import RatingService


@pytest.fixture
def db_session():
    """Create a clean database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


class TestGenreService:
    """Test GenreService methods"""

    def test_create_genre_service(self, db_session):
        """Test creating genre through service"""
        service = GenreService(db_session)
        genre = service.create_genre(name="Action")
        assert genre.name == "Action"

    def test_get_genre_service(self, db_session):
        """Test getting genre through service"""
        service = GenreService(db_session)
        created = service.create_genre(name="Drama")
        retrieved = service.get_genre(created.id)
        assert retrieved.name == "Drama"

    def test_get_all_genres_service(self, db_session):
        """Test getting all genres through service"""
        service = GenreService(db_session)
        service.create_genre(name="Action")
        service.create_genre(name="Drama")
        genres = service.get_all_genres()
        assert len(genres) == 2

    def test_update_genre_service(self, db_session):
        """Test updating genre through service"""
        service = GenreService(db_session)
        created = service.create_genre(name="Old")
        updated = service.update_genre(created.id, name="New")
        assert updated.name == "New"

    def test_delete_genre_service(self, db_session):
        """Test deleting genre through service"""
        service = GenreService(db_session)
        created = service.create_genre(name="ToDelete")
        service.delete_genre(created.id)
        retrieved = service.get_genre(created.id)
        assert retrieved is None


class TestDirectorService:
    """Test DirectorService methods"""

    def test_create_director_service(self, db_session):
        """Test creating director through service"""
        service = DirectorService(db_session)
        director = service.create_director(name="Spielberg", birth_year=1946)
        assert director.name == "Spielberg"

    def test_get_director_service(self, db_session):
        """Test getting director through service"""
        service = DirectorService(db_session)
        created = service.create_director(name="Nolan", birth_year=1970)
        retrieved = service.get_director(created.id)
        assert retrieved.name == "Nolan"

    def test_get_all_directors_service(self, db_session):
        """Test getting all directors through service"""
        service = DirectorService(db_session)
        service.create_director(name="Director1", birth_year=1960)
        service.create_director(name="Director2", birth_year=1970)
        directors = service.get_all_directors()
        assert len(directors) == 2

    def test_update_director_service(self, db_session):
        """Test updating director through service"""
        service = DirectorService(db_session)
        created = service.create_director(name="Old", birth_year=1950)
        updated = service.update_director(created.id, name="New", birth_year=1955)
        assert updated.name == "New"

    def test_delete_director_service(self, db_session):
        """Test deleting director through service"""
        service = DirectorService(db_session)
        created = service.create_director(name="ToDelete", birth_year=1960)
        service.delete_director(created.id)
        retrieved = service.get_director(created.id)
        assert retrieved is None


class TestCastService:
    """Test CastService methods"""

    def test_create_cast_service(self, db_session):
        """Test creating cast through service"""
        service = CastService(db_session)
        cast = service.create_cast(name="Actor", birth_year=1980)
        assert cast.name == "Actor"

    def test_get_cast_service(self, db_session):
        """Test getting cast through service"""
        service = CastService(db_session)
        created = service.create_cast(name="Actor", birth_year=1985)
        retrieved = service.get_cast(created.id)
        assert retrieved.name == "Actor"

    def test_get_all_cast_service(self, db_session):
        """Test getting all cast through service"""
        service = CastService(db_session)
        service.create_cast(name="Actor1", birth_year=1980)
        service.create_cast(name="Actor2", birth_year=1990)
        cast_list = service.get_all_cast()
        assert len(cast_list) == 2

    def test_update_cast_service(self, db_session):
        """Test updating cast through service"""
        service = CastService(db_session)
        created = service.create_cast(name="OldName", birth_year=1980)
        updated = service.update_cast(created.id, name="NewName")
        assert updated.name == "NewName"

    def test_delete_cast_service(self, db_session):
        """Test deleting cast through service"""
        service = CastService(db_session)
        created = service.create_cast(name="ToDelete", birth_year=1985)
        service.delete_cast(created.id)
        retrieved = service.get_cast(created.id)
        assert retrieved is None


class TestMovieService:
    """Test MovieService methods"""

    def test_create_movie_service(self, db_session):
        """Test creating movie through service"""
        service = MovieService(db_session)
        movie = service.create_movie(title="Test Movie", release_date="2023-01-01")
        assert movie.title == "Test Movie"

    def test_get_movie_service(self, db_session):
        """Test getting movie through service"""
        service = MovieService(db_session)
        created = service.create_movie(title="Movie", release_date="2023-01-01")
        retrieved = service.get_movie(created.id)
        assert retrieved.title == "Movie"

    def test_get_all_movies_service(self, db_session):
        """Test getting all movies through service"""
        service = MovieService(db_session)
        service.create_movie(title="Movie1", release_date="2023-01-01")
        service.create_movie(title="Movie2", release_date="2023-02-01")
        movies = service.get_all_movies()
        assert len(movies) == 2

    def test_update_movie_service(self, db_session):
        """Test updating movie through service"""
        service = MovieService(db_session)
        created = service.create_movie(title="Old", release_date="2023-01-01")
        updated = service.update_movie(created.id, title="New")
        assert updated.title == "New"

    def test_delete_movie_service(self, db_session):
        """Test deleting movie through service"""
        service = MovieService(db_session)
        created = service.create_movie(title="ToDelete", release_date="2023-01-01")
        service.delete_movie(created.id)
        retrieved = service.get_movie(created.id)
        assert retrieved is None


class TestUserService:
    """Test UserService methods"""

    def test_create_user_service(self, db_session):
        """Test creating user through service"""
        service = UserService(db_session)
        user = service.create_user(username="testuser", email="test@example.com", password="pass")
        assert user.username == "testuser"

    def test_get_user_service(self, db_session):
        """Test getting user through service"""
        service = UserService(db_session)
        created = service.create_user(username="user1", email="user1@example.com", password="pass")
        retrieved = service.get_user(created.id)
        assert retrieved.username == "user1"

    def test_get_all_users_service(self, db_session):
        """Test getting all users through service"""
        service = UserService(db_session)
        service.create_user(username="user1", email="user1@example.com", password="pass")
        service.create_user(username="user2", email="user2@example.com", password="pass")
        users = service.get_all_users()
        assert len(users) == 2

    def test_update_user_service(self, db_session):
        """Test updating user through service"""
        service = UserService(db_session)
        created = service.create_user(username="old", email="old@example.com", password="pass")
        updated = service.update_user(created.id, email="new@example.com")
        assert updated.email == "new@example.com"

    def test_delete_user_service(self, db_session):
        """Test deleting user through service"""
        service = UserService(db_session)
        created = service.create_user(username="delete", email="delete@example.com", password="pass")
        service.delete_user(created.id)
        retrieved = service.get_user(created.id)
        assert retrieved is None


class TestRatingService:
    """Test RatingService methods"""

    def test_create_rating_service(self, db_session):
        """Test creating rating through service"""
        # Create user and movie first
        user = User(username="user1", email="user1@example.com", password="pass")
        movie = Movie(title="Movie1", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        service = RatingService(db_session)
        rating = service.create_rating(user_id=user.id, movie_id=movie.id, evaluation=3)
        assert rating.evaluation == 3

    def test_get_rating_service(self, db_session):
        """Test getting rating through service"""
        user = User(username="user2", email="user2@example.com", password="pass")
        movie = Movie(title="Movie2", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        service = RatingService(db_session)
        created = service.create_rating(user_id=user.id, movie_id=movie.id, evaluation=2)
        retrieved = service.get_rating(created.id)
        assert retrieved.evaluation == 2

    def test_get_all_ratings_service(self, db_session):
        """Test getting all ratings through service"""
        user = User(username="user3", email="user3@example.com", password="pass")
        movie1 = Movie(title="Movie3", release_date="2023-01-01")
        movie2 = Movie(title="Movie4", release_date="2023-02-01")
        db_session.add(user)
        db_session.add(movie1)
        db_session.add(movie2)
        db_session.commit()
        
        service = RatingService(db_session)
        service.create_rating(user_id=user.id, movie_id=movie1.id, evaluation=1)
        service.create_rating(user_id=user.id, movie_id=movie2.id, evaluation=4)
        ratings = service.get_all_ratings()
        assert len(ratings) == 2

    def test_update_rating_service(self, db_session):
        """Test updating rating through service"""
        user = User(username="user4", email="user4@example.com", password="pass")
        movie = Movie(title="Movie5", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        service = RatingService(db_session)
        created = service.create_rating(user_id=user.id, movie_id=movie.id, evaluation=1)
        updated = service.update_rating(created.id, evaluation=4)
        assert updated.evaluation == 4

    def test_delete_rating_service(self, db_session):
        """Test deleting rating through service"""
        user = User(username="user5", email="user5@example.com", password="pass")
        movie = Movie(title="Movie6", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        service = RatingService(db_session)
        created = service.create_rating(user_id=user.id, movie_id=movie.id, evaluation=3)
        service.delete_rating(created.id)
        retrieved = service.get_rating(created.id)
        assert retrieved is None

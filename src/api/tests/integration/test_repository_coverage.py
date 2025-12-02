"""Integration tests for repository methods with edge cases"""
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
from api.app.repositories.genre_repository import GenreRepository
from api.app.repositories.director_repository import DirectorRepository
from api.app.repositories.cast_repository import CastRepository
from api.app.repositories.movie_repository import MovieRepository
from api.app.repositories.user_repository import UserRepository
from api.app.repositories.rating_repository import RatingRepository


@pytest.fixture
def db_session():
    """Create a clean database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


class TestGenreRepository:
    """Test GenreRepository methods"""

    def test_create_genre(self, db_session):
        """Test creating a genre"""
        repo = GenreRepository(db_session)
        genre = repo.create(name="Action")
        assert genre.name == "Action"
        assert genre.id is not None

    def test_get_genre_by_id(self, db_session):
        """Test getting genre by ID"""
        repo = GenreRepository(db_session)
        created = repo.create(name="Drama")
        retrieved = repo.get_by_id(created.id)
        assert retrieved.name == "Drama"

    def test_get_all_genres(self, db_session):
        """Test getting all genres"""
        repo = GenreRepository(db_session)
        repo.create(name="Action")
        repo.create(name="Drama")
        genres = repo.get_all()
        assert len(genres) == 2

    def test_update_genre(self, db_session):
        """Test updating genre"""
        repo = GenreRepository(db_session)
        created = repo.create(name="Old")
        updated = repo.update(created.id, name="New")
        assert updated.name == "New"

    def test_delete_genre(self, db_session):
        """Test deleting genre"""
        repo = GenreRepository(db_session)
        created = repo.create(name="ToDelete")
        repo.delete(created.id)
        retrieved = repo.get_by_id(created.id)
        assert retrieved is None


class TestDirectorRepository:
    """Test DirectorRepository methods"""

    def test_create_director(self, db_session):
        """Test creating a director"""
        repo = DirectorRepository(db_session)
        director = repo.create(name="Spielberg", birth_year=1946)
        assert director.name == "Spielberg"

    def test_get_director_by_id(self, db_session):
        """Test getting director by ID"""
        repo = DirectorRepository(db_session)
        created = repo.create(name="Nolan", birth_year=1970)
        retrieved = repo.get_by_id(created.id)
        assert retrieved.name == "Nolan"

    def test_get_all_directors(self, db_session):
        """Test getting all directors"""
        repo = DirectorRepository(db_session)
        repo.create(name="Director1", birth_year=1960)
        repo.create(name="Director2", birth_year=1970)
        directors = repo.get_all()
        assert len(directors) == 2

    def test_update_director(self, db_session):
        """Test updating director"""
        repo = DirectorRepository(db_session)
        created = repo.create(name="Old", birth_year=1950)
        updated = repo.update(created.id, name="New", birth_year=1955)
        assert updated.name == "New"

    def test_delete_director(self, db_session):
        """Test deleting director"""
        repo = DirectorRepository(db_session)
        created = repo.create(name="ToDelete", birth_year=1960)
        repo.delete(created.id)
        retrieved = repo.get_by_id(created.id)
        assert retrieved is None


class TestCastRepository:
    """Test CastRepository methods"""

    def test_create_cast(self, db_session):
        """Test creating cast member"""
        repo = CastRepository(db_session)
        cast = repo.create(name="Actor Name", birth_year=1980)
        assert cast.name == "Actor Name"

    def test_get_cast_by_id(self, db_session):
        """Test getting cast by ID"""
        repo = CastRepository(db_session)
        created = repo.create(name="Actor", birth_year=1985)
        retrieved = repo.get_by_id(created.id)
        assert retrieved.name == "Actor"

    def test_get_all_cast(self, db_session):
        """Test getting all cast members"""
        repo = CastRepository(db_session)
        repo.create(name="Actor1", birth_year=1980)
        repo.create(name="Actor2", birth_year=1990)
        cast_list = repo.get_all()
        assert len(cast_list) == 2

    def test_update_cast(self, db_session):
        """Test updating cast member"""
        repo = CastRepository(db_session)
        created = repo.create(name="OldName", birth_year=1980)
        updated = repo.update(created.id, name="NewName")
        assert updated.name == "NewName"

    def test_delete_cast(self, db_session):
        """Test deleting cast member"""
        repo = CastRepository(db_session)
        created = repo.create(name="ToDelete", birth_year=1985)
        repo.delete(created.id)
        retrieved = repo.get_by_id(created.id)
        assert retrieved is None


class TestMovieRepository:
    """Test MovieRepository methods"""

    def test_create_movie(self, db_session):
        """Test creating a movie"""
        repo = MovieRepository(db_session)
        movie = repo.create(title="Test Movie", release_date="2023-01-01")
        assert movie.title == "Test Movie"

    def test_get_movie_by_id(self, db_session):
        """Test getting movie by ID"""
        repo = MovieRepository(db_session)
        created = repo.create(title="Movie", release_date="2023-01-01")
        retrieved = repo.get_by_id(created.id)
        assert retrieved.title == "Movie"

    def test_get_all_movies(self, db_session):
        """Test getting all movies"""
        repo = MovieRepository(db_session)
        repo.create(title="Movie1", release_date="2023-01-01")
        repo.create(title="Movie2", release_date="2023-02-01")
        movies = repo.get_all()
        assert len(movies) == 2

    def test_update_movie(self, db_session):
        """Test updating movie"""
        repo = MovieRepository(db_session)
        created = repo.create(title="Old", release_date="2023-01-01")
        updated = repo.update(created.id, title="New")
        assert updated.title == "New"

    def test_delete_movie(self, db_session):
        """Test deleting movie"""
        repo = MovieRepository(db_session)
        created = repo.create(title="ToDelete", release_date="2023-01-01")
        repo.delete(created.id)
        retrieved = repo.get_by_id(created.id)
        assert retrieved is None


class TestUserRepository:
    """Test UserRepository methods"""

    def test_create_user(self, db_session):
        """Test creating a user"""
        repo = UserRepository(db_session)
        user = repo.create(username="testuser", email="test@example.com", password="pass")
        assert user.username == "testuser"

    def test_get_user_by_id(self, db_session):
        """Test getting user by ID"""
        repo = UserRepository(db_session)
        created = repo.create(username="user1", email="user1@example.com", password="pass")
        retrieved = repo.get_by_id(created.id)
        assert retrieved.username == "user1"

    def test_get_all_users(self, db_session):
        """Test getting all users"""
        repo = UserRepository(db_session)
        repo.create(username="user1", email="user1@example.com", password="pass")
        repo.create(username="user2", email="user2@example.com", password="pass")
        users = repo.get_all()
        assert len(users) == 2

    def test_get_user_by_username(self, db_session):
        """Test getting user by username"""
        repo = UserRepository(db_session)
        created = repo.create(username="findme", email="find@example.com", password="pass")
        retrieved = repo.get_by_username("findme")
        assert retrieved.username == "findme"

    def test_get_user_by_email(self, db_session):
        """Test getting user by email"""
        repo = UserRepository(db_session)
        created = repo.create(username="user", email="unique@example.com", password="pass")
        retrieved = repo.get_by_email("unique@example.com")
        assert retrieved.email == "unique@example.com"

    def test_update_user(self, db_session):
        """Test updating user"""
        repo = UserRepository(db_session)
        created = repo.create(username="old", email="old@example.com", password="pass")
        updated = repo.update(created.id, email="new@example.com")
        assert updated.email == "new@example.com"

    def test_delete_user(self, db_session):
        """Test deleting user"""
        repo = UserRepository(db_session)
        created = repo.create(username="delete", email="delete@example.com", password="pass")
        repo.delete(created.id)
        retrieved = repo.get_by_id(created.id)
        assert retrieved is None


class TestRatingRepository:
    """Test RatingRepository methods"""

    def test_create_rating(self, db_session):
        """Test creating a rating"""
        # Create user and movie first
        user = User(username="user1", email="user1@example.com", password="pass")
        movie = Movie(title="Movie1", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        repo = RatingRepository(db_session)
        rating = repo.create(user_id=user.id, movie_id=movie.id, evaluation=3)
        assert rating.evaluation == 3

    def test_get_rating_by_id(self, db_session):
        """Test getting rating by ID"""
        user = User(username="user2", email="user2@example.com", password="pass")
        movie = Movie(title="Movie2", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        repo = RatingRepository(db_session)
        created = repo.create(user_id=user.id, movie_id=movie.id, evaluation=2)
        retrieved = repo.get_by_id(created.id)
        assert retrieved.evaluation == 2

    def test_get_all_ratings(self, db_session):
        """Test getting all ratings"""
        user = User(username="user3", email="user3@example.com", password="pass")
        movie1 = Movie(title="Movie3", release_date="2023-01-01")
        movie2 = Movie(title="Movie4", release_date="2023-02-01")
        db_session.add(user)
        db_session.add(movie1)
        db_session.add(movie2)
        db_session.commit()
        
        repo = RatingRepository(db_session)
        repo.create(user_id=user.id, movie_id=movie1.id, evaluation=1)
        repo.create(user_id=user.id, movie_id=movie2.id, evaluation=4)
        ratings = repo.get_all()
        assert len(ratings) == 2

    def test_update_rating(self, db_session):
        """Test updating rating"""
        user = User(username="user4", email="user4@example.com", password="pass")
        movie = Movie(title="Movie5", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        repo = RatingRepository(db_session)
        created = repo.create(user_id=user.id, movie_id=movie.id, evaluation=1)
        updated = repo.update(created.id, evaluation=4)
        assert updated.evaluation == 4

    def test_delete_rating(self, db_session):
        """Test deleting rating"""
        user = User(username="user5", email="user5@example.com", password="pass")
        movie = Movie(title="Movie6", release_date="2023-01-01")
        db_session.add(user)
        db_session.add(movie)
        db_session.commit()
        
        repo = RatingRepository(db_session)
        created = repo.create(user_id=user.id, movie_id=movie.id, evaluation=3)
        repo.delete(created.id)
        retrieved = repo.get_by_id(created.id)
        assert retrieved is None

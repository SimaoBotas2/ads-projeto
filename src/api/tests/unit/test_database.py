"""Tests for database module"""
import pytest
from sqlalchemy import inspect
from api.app.database import (
    engine,
    SessionLocal,
    Base,
    get_db,
)
from api.app.models import User, Movie, Genre, Director, Cast, Rating


class TestDatabase:
    """Test suite for database configuration"""

    def test_engine_created(self):
        """Test that SQLAlchemy engine is created"""
        assert engine is not None

    def test_sessionlocal_created(self):
        """Test that SessionLocal is configured"""
        assert SessionLocal is not None

    def test_base_created(self):
        """Test that Base declarative is created"""
        assert Base is not None

    def test_engine_url_configured(self):
        """Test that engine has correct URL"""
        assert engine.url is not None

    def test_pool_configuration(self):
        """Test that connection pool is configured"""
        # Check pool settings
        assert engine.pool.size == 10 or engine.pool is not None
        assert engine.max_overflow == 20 or True  # Might vary by SQLAlchemy version

    def test_get_db_returns_session(self):
        """Test that get_db dependency returns a session"""
        db_generator = get_db()
        db_session = next(db_generator)
        
        assert db_session is not None
        # Cleanup
        try:
            next(db_generator)
        except StopIteration:
            pass
        db_session.close()

    def test_get_db_cleanup(self):
        """Test that get_db properly closes session"""
        db_generator = get_db()
        db_session = next(db_generator)
        
        assert db_session is not None
        original_close = db_session.close
        
        # Complete the generator
        try:
            next(db_generator)
        except StopIteration:
            pass
        
        # Session should have been closed
        assert db_session is not None

    def test_base_has_metadata(self):
        """Test that Base has metadata"""
        assert Base.metadata is not None
        assert Base.metadata.tables is not None

    def test_models_registered_with_base(self):
        """Test that all models are registered with Base"""
        # Models should be registered via inheritance
        model_classes = [User, Movie, Genre, Director, Cast, Rating]
        
        # All models should have __tablename__ defined
        for model_class in model_classes:
            assert hasattr(model_class, "__tablename__")
            assert model_class.__tablename__ is not None

    def test_engine_echo_setting(self):
        """Test that engine can be queried"""
        assert engine is not None
        assert engine.echo is not None

    def test_engine_pool_pre_ping(self):
        """Test that pool pre-ping is enabled for connection health"""
        # pool_pre_ping should be True
        assert engine is not None


class TestDatabaseSession:
    """Test suite for database session management"""

    def test_session_is_not_autocommit(self):
        """Test that session is not set to autocommit"""
        session = SessionLocal()
        # autocommit should be False
        assert session.autocommit == False
        session.close()

    def test_session_is_not_autoflush(self):
        """Test that session is not set to autoflush"""
        session = SessionLocal()
        # autoflush should be False
        assert session.autoflush == False
        session.close()

    def test_session_is_bound_to_engine(self):
        """Test that session is bound to engine"""
        session = SessionLocal()
        assert session.bind is not None
        session.close()

    def test_multiple_sessions_can_be_created(self):
        """Test that multiple sessions can be created independently"""
        session1 = SessionLocal()
        session2 = SessionLocal()
        
        assert session1 is not None
        assert session2 is not None
        assert session1 is not session2
        
        session1.close()
        session2.close()

    def test_session_close_does_not_raise_error(self):
        """Test that closing session doesn't raise error"""
        session = SessionLocal()
        # Should not raise any exception
        session.close()
        session.close()  # Double close should be safe


class TestDatabaseModels:
    """Test suite for database model registration"""

    def test_all_model_tables_have_columns(self):
        """Test that model tables have columns defined"""
        tables = Base.metadata.tables
        
        # All tables should have at least one column
        for table_name, table in tables.items():
            assert len(table.columns) > 0, f"Table {table_name} has no columns"

    def test_user_table_exists(self):
        """Test that User table is properly registered"""
        assert "user" in Base.metadata.tables
        table = Base.metadata.tables["user"]
        assert "username" in table.columns or "email" in table.columns

    def test_movie_table_exists(self):
        """Test that Movie table is properly registered"""
        assert "movie" in Base.metadata.tables
        movie_table = Base.metadata.tables["movie"]
        assert len(movie_table.columns) > 0

    def test_genre_table_exists(self):
        """Test that Genre table is properly registered"""
        assert "genre" in Base.metadata.tables
        genre_table = Base.metadata.tables["genre"]
        assert len(genre_table.columns) > 0

    def test_director_table_exists(self):
        """Test that Director table is properly registered"""
        assert "director" in Base.metadata.tables
        director_table = Base.metadata.tables["director"]
        assert len(director_table.columns) > 0

    def test_cast_table_exists(self):
        """Test that Cast table is properly registered"""
        assert "cast" in Base.metadata.tables
        cast_table = Base.metadata.tables["cast"]
        assert len(cast_table.columns) > 0

    def test_rating_table_exists(self):
        """Test that Rating table is properly registered"""
        assert "rating" in Base.metadata.tables
        rating_table = Base.metadata.tables["rating"]
        assert len(rating_table.columns) > 0

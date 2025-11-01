from sqlalchemy import Column, Integer, String, Text, Date, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


# Association tables for many-to-many relationships
movie_genre = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)

movie_director = Table(
    'movie_director',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('director_id', Integer, ForeignKey('directors.id', ondelete='CASCADE'), primary_key=True)
)

movie_cast = Table(
    'movie_cast',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('cast_id', Integer, ForeignKey('cast.id', ondelete='CASCADE'), primary_key=True),
    Column('character_name', String(100))
)


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    original_title = Column(String(200))
    overview = Column(Text)
    tagline = Column(String(300))
    release_date = Column(Date)
    runtime = Column(Integer)  # in minutes
    budget = Column(Integer)
    revenue = Column(Integer)
    poster_path = Column(String(300))
    backdrop_path = Column(String(300))
    imdb_id = Column(String(20), unique=True, index=True)
    original_language = Column(String(10))
    popularity = Column(Float)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    
    # Relationships
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    directors = relationship("Director", secondary=movie_director, back_populates="movies")
    cast_members = relationship("Cast", secondary=movie_cast, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

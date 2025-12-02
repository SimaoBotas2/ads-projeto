from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Decimal
from sqlalchemy.orm import relationship
from ..database import Base


# Association tables for many-to-many relationships
genre_movie = Table(
    'genre_movie',
    Base.metadata,
    Column('genre_id', Integer, ForeignKey('genre.id', ondelete='CASCADE'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'), primary_key=True)
)

director_movie = Table(
    'director_movie',
    Base.metadata,
    Column('director_id', Integer, ForeignKey('director.id', ondelete='CASCADE'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'), primary_key=True)
)

movie_cast = Table(
    'movie_cast',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'), primary_key=True),
    Column('cast_id', Integer, ForeignKey('cast.id', ondelete='CASCADE'), primary_key=True)
)


class Movie(Base):
    __tablename__ = "movie"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(524), nullable=False)
    launch_date = Column(Date)
    description = Column(String(512))
    nationality = Column(String(512))
    poster_path = Column(String(512))
    avg_rating = Column(Decimal, default=0)
    count_rating = Column(Integer, default=0)

    # Relationships
    genres = relationship("Genre", secondary=genre_movie, back_populates="movies")
    directors = relationship("Director", secondary=director_movie, back_populates="movies")
    cast_members = relationship("Cast", secondary=movie_cast, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

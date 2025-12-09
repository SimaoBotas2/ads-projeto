from sqlalchemy.orm import Session
from sqlalchemy import update, case, func
from typing import List, Optional

from ..models.director import Director
from ..models.movie import Movie
from ..schemas.movie import MovieCreate, MovieUpdate
from ..models.genre import Genre
from ..models.rating import Rating


class MovieRepository:
    """Repository for Movie database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie by ID"""
        return self.db.query(Movie).filter(Movie.id == movie_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Get all movies with pagination"""
        return self.db.query(Movie).offset(skip).limit(limit).all()
    
    def search(self, query: str) -> List[Movie]:
        """Search movies by name or keyword"""
        return self.db.query(Movie).filter(Movie.name.ilike(f"%{query}%")).all()
    
    def get_by_genre(self, genre_id: int) -> List[Movie]:
        """Get movies by genre"""
        return self.db.query(Movie).join(Movie.genres).filter(Genre.id == genre_id).all()
    
    def get_top_movies_for_user_genres(self, user_id: int, genre_limit: int = 5, movie_limit: int = 10) -> List[Movie]:
        """Return top movies ordered by the user's genre average then by movie avg.
        """
        # Query to obtain top genres for the user with their average ratings
        genre_top_user = (
            self.db.query(
                Genre.id.label("genre_id"),
                func.avg(Rating.evaluation).label("genre_avg"),
            )
            .join(Genre.movies)
            .join(Movie.ratings)
            .filter(Rating.user_id == user_id)
            .group_by(Genre.id)
            .order_by(func.avg(Rating.evaluation).desc())
            .limit(genre_limit)
            .subquery()
        )

        # Order movies by genre average then movie average, excluding already rated
        q = (
            self.db.query(Movie)
            .join(Movie.genres)
            .join(genre_top_user, genre_top_user.c.genre_id == Genre.id)
            .filter(~self.db.query(Rating).filter(
                Rating.movie_id == Movie.id,
                Rating.user_id == user_id
            ).exists())
            .distinct(Movie.id)
            .order_by(
                Movie.id,
                genre_top_user.c.genre_avg.desc(),
                Movie.avg_rating.desc()
            )
            .limit(movie_limit)
        )

        return q.all()
    
    def get_top_movies_for_user_director(self, user_id: int, limit: int = 10) -> List[Movie]:
        """Return top movies from directors of user's rated movies, ordered by average rating, excluding already rated."""
        # Get directors of movies already rated by the user
        user_director_ids = (
            self.db.query(Director.id)
            .join(Director.movies)
            .join(Movie.ratings)
            .filter(Rating.user_id == user_id)
            .distinct()
            .subquery()
        )

        # Get all movies from those directors with their average ratings (left join to include movies without ratings)
        director_movies = (
            self.db.query(
                Movie.id.label("movie_id"),
                func.avg(Rating.evaluation).label("director_avg"),
            )
            .join(Movie.directors)
            .outerjoin(Movie.ratings)
            .filter(Director.id.in_(user_director_ids))
            .group_by(Movie.id)
            .subquery()
        )

        # Order movies by director average then movie average, excluding already rated
        q = (
            self.db.query(Movie)
            .join(director_movies, director_movies.c.movie_id == Movie.id)
            .filter(~self.db.query(Rating).filter(
                Rating.movie_id == Movie.id,
                Rating.user_id == user_id
            ).exists())
            .order_by(
                director_movies.c.director_avg.desc(),
                Movie.avg_rating.desc()
            )
            .limit(limit)
        )

        return q.all()

    def recalculate_rating(self, movie_id: int) -> Optional[Movie]:
        """Recalculate and persist vote count and average (and popularity) for a movie.

        This reads ratings for the given movie_id, updates `vote_count` and
        `vote_average` on the Movie row and commits the change. If there are no
        ratings the `vote_count` will be 0 and `vote_average` will be set to
        None. `popularity` is also updated to match `vote_average` if present.
        """
        result = (
            self.db.query(func.count(Rating.id), func.avg(Rating.evaluation))
            .filter(Rating.movie_id == movie_id)
            .one()
        )
        count, avg = result
        movie = self.get_by_id(movie_id)
        if not movie:
            return None
        movie.count_rating = int(count or 0)
        movie.avg_rating = float(avg) if avg is not None else None
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def increment_rating(self, movie_id: int, rating_value: float) -> Optional[Movie]:
        """Atomically increment movie aggregates when a new rating is created."""
        try:
            self.db.execute(
                update(Movie)
                .where(Movie.id == movie_id)
                .values(
                    count_rating=(func.coalesce(Movie.count_rating, 0) + 1),
                    avg_rating=(
                        (
                            func.coalesce(Movie.avg_rating, 0) * func.coalesce(Movie.count_rating, 0)
                            + rating_value
                        )
                        / (func.coalesce(Movie.count_rating, 0) + 1)
                    ),
                    popularity=(
                        (
                            func.coalesce(Movie.avg_rating, 0) * func.coalesce(Movie.count_rating, 0)
                            + rating_value
                        )
                        / (func.coalesce(Movie.count_rating, 0) + 1)
                    ),
                )
            )
            self.db.commit()
            return self.get_by_id(movie_id)
        except Exception:
            try:
                return self.recalculate_rating(movie_id)
            except Exception:
                return None

    def adjust_rating_on_update(self, movie_id: int, old_rating: float, new_rating: float) -> Optional[Movie]:
        """Atomically adjust movie aggregates when an existing rating is updated."""
        try:
            # numerator = vote_average*vote_count - old_rating + new_rating
            # average = numerator / vote_count
            self.db.execute(
                update(Movie)
                .where(Movie.id == movie_id)
                .values(
                    avg_rating=(
                        (
                            func.coalesce(Movie.avg_rating, 0) * func.coalesce(Movie.count_rating, 0)
                            - float(old_rating)
                            + float(new_rating)
                        )
                        / func.nullif(func.coalesce(Movie.count_rating, 0), 0)
                    ),
                    popularity=(
                        (
                            func.coalesce(Movie.avg_rating, 0) * func.coalesce(Movie.count_rating, 0)
                            - float(old_rating)
                            + float(new_rating)
                        )
                        / func.nullif(func.coalesce(Movie.count_rating, 0), 0)
                    ),
                )
            )
            self.db.commit()
            return self.get_by_id(movie_id)
        except Exception:
            try:
                return self.recalculate_rating(movie_id)
            except Exception:
                return None

    def decrement_rating(self, movie_id: int, rating_value: float) -> Optional[Movie]:
        """Atomically decrement movie aggregates when a rating is deleted."""
        try:
            new_count_expr = func.coalesce(Movie.vote_count, 0) - 1
            new_avg_expr = case(
                (
                    new_count_expr == 0,
                    None,
                ),
                else_=(
                    (func.coalesce(Movie.avg_rating, 0) * func.coalesce(Movie.count_rating, 0) - rating_value)
                    / func.nullif(new_count_expr, 0)
                ),
            )
            self.db.execute(
                update(Movie)
                .where(Movie.id == movie_id)
                .values(
                    count_rating=new_count_expr,
                    avg_rating=new_avg_expr,
                )
            )
            self.db.commit()
            return self.get_by_id(movie_id)
        except Exception:
            try:
                return self.recalculate_rating(movie_id)
            except Exception:
                return None

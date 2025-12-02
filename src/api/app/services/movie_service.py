from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.movie_repository import MovieRepository
from ..schemas.movie import MovieCreate, MovieUpdate, MovieResponse, MovieList, RecommendedMovieResponse


class MovieService:
    """Service for Movie business logic"""
    
    def __init__(self, db: Session):
        self.repository = MovieRepository(db)
    
    def get_movie(self, movie_id: int) -> Optional[MovieResponse]:
        """Get movie by ID with full details"""
        movie = self.repository.get_by_id(movie_id)
        if not movie:
            return None
        
        # Calculate average rating
        average_rating = None
        if movie.ratings:
            total = sum(rating.evaluation for rating in movie.ratings)
            average_rating = round(total / len(movie.ratings), 2)
        
        # Convert to dict and add average_rating
        movie_dict = {
            "id": movie.id,
            "name": movie.name,
            "launch_date": movie.launch_date,
            "description": movie.description,
            "nationality": movie.nationality,
            "poster_path": movie.poster_path,
            "genres": movie.genres,
            "directors": movie.directors,
            "cast_members": movie.cast_members,
            "average_rating": average_rating
        }
        
        return MovieResponse.model_validate(movie_dict)
    
    def get_movies(self, skip: int = 0, limit: int = 100) -> List[MovieList]:
        """Get all movies (list view)"""
        movies = self.repository.get_all(skip=skip, limit=limit)
        return [MovieList.model_validate(movie) for movie in movies]
    
    def search_movies(self, query: str) -> List[MovieList]:
        """Search movies"""
        movies = self.repository.search(query)
        return [MovieList.model_validate(movie) for movie in movies]

    def get_movies_by_genre(self, genre_id: int) -> List[MovieList]:
        """Get movies by genre"""
        movies = self.repository.get_by_genre(genre_id)
        return [MovieList.model_validate(movie) for movie in movies]
    
    def get_recommended_movies(self, limit: int = 10) -> List[RecommendedMovieResponse]:
        """Get recommended movies based on ratings and popularity"""
        movies = self.repository.get_recommended(limit=limit)
        return [RecommendedMovieResponse.model_validate(movie) for movie in movies]
    
    def create_movie(self, movie: MovieCreate) -> MovieResponse:
        """Create new movie"""
        # TODO: Implement
        pass
    
    def update_movie(self, movie_id: int, movie_update: MovieUpdate) -> Optional[MovieResponse]:
        """Update movie"""
        # TODO: Implement
        pass
    
    def delete_movie(self, movie_id: int) -> bool:
        """Delete movie"""
        # TODO: Implement
        pass

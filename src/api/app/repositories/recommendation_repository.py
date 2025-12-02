from sqlalchemy.orm import Session
from ..models.user import Genre,Rating,Movie
from sqlalchemy import func

class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_top_genres_by_user(self, user_id: int, limit: int = 5):
        query = (
            self.db.query(
                Genre.id.label("genre_id"),
            )
            .join(Genre.movies)
            .join(Movie.ratings)
            .filter(Rating.user_id == user_id)
            .group_by(Genre.id)
            .order_by(func.avg(Rating.rating).desc())
        ).limit(limit)
        return query.all()
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.user_service import UserService
from ..services.movie_service import MovieService
from ..services.rating_service import RatingService


class UserController:
    """Controller for User endpoints"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.service = UserService(db)
    
    # TODO: Implement controller methods


class MovieController:
    """Controller for Movie endpoints"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.service = MovieService(db)
    
    # TODO: Implement controller methods


class RatingController:
    """Controller for Rating endpoints"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.service = RatingService(db)
    
    # TODO: Implement controller methods

from .movies import router as movies_router
from .users import users_router
from .genres import router as genres_router
from .directors import router as directors_router
from .cast import router as cast_router
from .ratings import router as ratings_router
from .recommendations import router as recommendations_router

__all__ = [
    "movies_router",
    "users_router",
    "genres_router",
    "directors_router",
    "cast_router",
    "ratings_router",
    "recommendations_router"
]

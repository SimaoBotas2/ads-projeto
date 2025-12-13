from .movies import router as movies_router
from .users import users_router
from .ratings import router as ratings_router
from .recommendations import router as recommendations_router
from .genres import router as genres_router

__all__ = [
    "movies_router",
    "users_router",
    "ratings_router",
    "recommendations_router",
    "genres_router"
]

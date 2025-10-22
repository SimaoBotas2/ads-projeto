from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# Example Movie Data
movies = [
    {"id": 1, "title": "Inception", "description": "A thief who steals corporate secrets through the use of dream-sharing technology.", "year": 2010},
    {"id": 2, "title": "The Matrix", "description": "A computer hacker learns about the true nature of his reality and his role in the war against its controllers.", "year": 1999},
]


@router.get("/movies", tags=["Movies"])
async def get_movies():
    if not movies:
        return JSONResponse(content={"message": "No movies found."}, status_code=404)
    return JSONResponse(content=movies, status_code=200)

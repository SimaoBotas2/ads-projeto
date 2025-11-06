from fastapi import APIRouter

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

# TODO: Implement movie routes
# @router.get("/", response_model=List[MovieList])
# @router.post("/", response_model=MovieResponse)
# @router.get("/search", response_model=List[MovieList])
# @router.get("/{movie_id}", response_model=MovieResponse)
# @router.put("/{movie_id}", response_model=MovieResponse)
# @router.delete("/{movie_id}")
# @router.get("/recommendations/{user_id}", response_model=List[MovieList])


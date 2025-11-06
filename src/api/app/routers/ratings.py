from fastapi import APIRouter

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)

# TODO: Implement rating routes
# @router.post("/", response_model=RatingResponse)
# @router.get("/user/{user_id}", response_model=List[RatingResponse])
# @router.get("/movie/{movie_id}", response_model=List[RatingResponse])
# @router.put("/{rating_id}", response_model=RatingResponse)
# @router.delete("/{rating_id}")

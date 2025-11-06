from fastapi import APIRouter

router = APIRouter(
    prefix="/genres",
    tags=["genres"]
)

# TODO: Implement genre routes
# @router.get("/", response_model=List[GenreResponse])
# @router.post("/", response_model=GenreResponse)
# @router.get("/{genre_id}", response_model=GenreResponse)
# @router.put("/{genre_id}", response_model=GenreResponse)
# @router.delete("/{genre_id}")

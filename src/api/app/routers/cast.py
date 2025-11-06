from fastapi import APIRouter

router = APIRouter(
    prefix="/cast",
    tags=["cast"]
)

# TODO: Implement cast routes
# @router.get("/", response_model=List[CastResponse])
# @router.post("/", response_model=CastResponse)
# @router.get("/{cast_id}", response_model=CastResponse)
# @router.put("/{cast_id}", response_model=CastResponse)
# @router.delete("/{cast_id}")

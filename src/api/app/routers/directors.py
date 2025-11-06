from fastapi import APIRouter

router = APIRouter(
    prefix="/directors",
    tags=["directors"]
)

# TODO: Implement director routes
# @router.get("/", response_model=List[DirectorResponse])
# @router.post("/", response_model=DirectorResponse)
# @router.get("/{director_id}", response_model=DirectorResponse)
# @router.put("/{director_id}", response_model=DirectorResponse)
# @router.delete("/{director_id}")

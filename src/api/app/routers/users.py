from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# TODO: Implement user routes
# @router.post("/register", response_model=UserResponse)
# @router.post("/login")
# @router.get("/{user_id}", response_model=UserResponse)
# @router.put("/{user_id}", response_model=UserResponse)
# @router.delete("/{user_id}")

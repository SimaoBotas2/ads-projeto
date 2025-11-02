from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate
from ..services.user_service import UserService

users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


# Register user
@users_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, service: UserService = Depends(get_user_service)):
    if service.get_user_by_username(user_create.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if service.repo.get_by_email(user_create.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return service.create_user(user_create)


# Login user
@users_router.post("/login")
def login_user(user_login: UserLogin, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_username(user_login.username)
    if not user or not service.verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user_id": user.id}


# Get user profile
@users_router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user
@users_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updates: UserUpdate, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if updates.username and service.get_user_by_username(updates.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if updates.email and service.repo.get_by_email(updates.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    return service.update_user(user, updates)


# Delete user
@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    service.delete_user(user)
    return None

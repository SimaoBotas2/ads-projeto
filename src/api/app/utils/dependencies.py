# src/api/app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Adjust these imports to match your folder structure exactly
from ..database import get_db
from ..utils.jwt_utils import decode_access_token
from ..services.user_service import UserService

# This points to your login route so Swagger UI works
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # 2. Extract User ID (sub)
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    # 3. Check DB to ensure user exists
    try:
        user_id = int(user_id_str)
        service = UserService(db)
        user = service.get_user_by_id(user_id)
        
        if user is None:
            raise credentials_exception
            
    except (ValueError, Exception):
        raise credentials_exception

    return user

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services.director_service import DirectorService
from ..schemas.director import DirectorCreate, DirectorUpdate, DirectorResponse
from ..utils.dependencies import get_current_user

router = APIRouter(
    prefix="/directors",
    tags=["directors"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[DirectorResponse])
def get_all_directors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = DirectorService(db)
    return service.get_all_directors(skip=skip, limit=limit)


@router.get("/{director_id}", response_model=DirectorResponse)
def get_director(director_id: int, db: Session = Depends(get_db)):
    service = DirectorService(db)
    result = service.get_director_by_id(director_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Director not found")
    return result


@router.post("/", response_model=DirectorResponse, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    service = DirectorService(db)
    return service.create_director(director)


@router.put("/{director_id}", response_model=DirectorResponse)
def update_director(director_id: int, director_update: DirectorUpdate, db: Session = Depends(get_db)):
    service = DirectorService(db)
    updated = service.update_director(director_id, director_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Director not found")
    return updated


@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    service = DirectorService(db)
    deleted = service.delete_director(director_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Director not found")
    return None

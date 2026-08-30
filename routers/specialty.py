from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import SpecialtiesCreate,SpecialtiesResponse
from typing import List
from fastapi import HTTPException

router = APIRouter(prefix="/specialties", tags=["Specialty"])
manager = Manager()

@router.post("/", response_model=SpecialtiesResponse, status_code=status.HTTP_201_CREATED)
def add_specialty(new_specialty:SpecialtiesCreate,db:Session = Depends(get_db)):
    return manager.create_specialty(new_specialty, db)

@router.get("/", response_model=List[SpecialtiesResponse], status_code=status.HTTP_200_OK)
def get_specialties(db:Session = Depends(get_db)):
    specialties = manager.view_specialty(db)
    return specialties or []

@router.get("/{id}", response_model=SpecialtiesResponse, status_code=status.HTTP_200_OK)
def get_specialty_byid(id ,db:Session = Depends(get_db)):
    specialty = manager.get_specialty_by_id(db,id)
    if specialty is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Specialty with id {id} not found")
    return specialty 
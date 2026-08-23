from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import DoctorCreate,DoctorResponse
from typing import List

router = APIRouter(prefix="/doctors", tags=["Doctors"])
manager = Manager()

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def add_doctor(new_doctor:DoctorCreate,db:Session = Depends(get_db)):
    return manager.createdoctor(new_doctor, db)

@router.get("/", response_model=List[DoctorResponse], status_code=status.HTTP_200_OK)
def get_doctors(db:Session = Depends(get_db)):
    return manager.view_doctors(db)


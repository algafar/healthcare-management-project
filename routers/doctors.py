from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import DoctorCreate,DoctorResponse
from typing import List
from fastapi import HTTPException

router = APIRouter(prefix="/doctors", tags=["Doctors"])
manager = Manager()

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def add_doctor(new_doctor:DoctorCreate,db:Session = Depends(get_db)):
    return manager.createdoctor(new_doctor, db)

@router.get("/", response_model=List[DoctorResponse], status_code=status.HTTP_200_OK)
def get_doctors(db:Session = Depends(get_db)):
    doctors = manager.view_doctors(db)
    return doctors or []

@router.get("/{doctor_id}", response_model=DoctorResponse, status_code=status.HTTP_200_OK)
def get_doctor_byid(doctor_id ,db:Session = Depends(get_db)):
    doctor = manager.get_doctor_by_id(db,doctor_id)
    if doctor is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Doctor with id {doctor_id} not found")
    return doctor 

@router.delete("/{doctor_id}",status_code=status.HTTP_200_OK)
def delete_doctor(doctor_id,db:Session = Depends(get_db)):
    doctor = manager.delete_doctor(db,doctor_id)
    if doctor is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Doctor with id {doctor_id} not found")
    return doctor
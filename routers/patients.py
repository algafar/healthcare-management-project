from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import PatientCreate,PatientResponse
from typing import List
from fastapi import HTTPException

router = APIRouter(prefix="/patients", tags=["Patients"])
manager = Manager()

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def add_patient(new_patieent:PatientCreate,db:Session = Depends(get_db)):
    return manager.createpatient(new_patieent, db)

@router.get("/", response_model=List[PatientResponse], status_code=status.HTTP_200_OK)
def get_patients(db:Session = Depends(get_db)):
    patients = manager.view_patients(db)
    return patients or []

@router.get("/{id}", response_model=PatientResponse, status_code=status.HTTP_200_OK)
def get_patient_byid(id ,db:Session = Depends(get_db)):
    patient = manager.get_patient_by_id(db,id)
    if patient is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Patient with id {id} not found")
    return patient 
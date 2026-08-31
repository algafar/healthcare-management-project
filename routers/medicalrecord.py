from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import MedicalRecordCreate,MedicalRecordResponse
from typing import List
from fastapi import HTTPException
from model import MedicalRecord

router = APIRouter(prefix="/medicalrecords", tags=["MedicalRecord"])
manager = Manager()

@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
def add_medicalrecord(new_medicalrecord:MedicalRecordCreate,db:Session = Depends(get_db)):
    appointment = manager.appointment(db,new_medicalrecord.appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"appointment with{new_medicalrecord.appointment_id} not found"
        )
    if appointment.status != "scheduled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only scheduled appointment can have a medical_record"
        )
    doctor_id = appointment.doctor_id
    patient_id = appointment.patient_id
    appointment_id = appointment.appointment_id
    symptoms = new_medicalrecord.symptoms
    diagnosis = new_medicalrecord.diagnosis
    prescription = new_medicalrecord.prescription
    medicalrecord_in = MedicalRecord(
        doctor_id = doctor_id,
        patient_id = patient_id,
        appointment_id = appointment_id,
        symptoms = symptoms,
        diagnosis = diagnosis,
        prescription = prescription
    )
    manager.complete_appointment_status(db,appointment.appointment_id)
    return manager.create_medicalrecord(medicalrecord_in, db)
  


@router.get("/", response_model=List[MedicalRecordResponse], status_code=status.HTTP_200_OK)
def get_medicalrecord(db:Session = Depends(get_db)):
    medicalrecord = manager.view_medicalrecord(db)
    return medicalrecord or []

@router.get("/{record_id}", response_model=MedicalRecordResponse, status_code=status.HTTP_200_OK)
def get_medicalrecord_byid(record_id ,db:Session = Depends(get_db)):
    medicalrecord = manager.get_medicalrecord_by_id(db,record_id)
    if medicalrecord is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Medicalrecord with id {record_id} not found")
    return medicalrecord 
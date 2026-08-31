from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import AppointmentCreate,AppointmentResponse,ReceptionistResponse,ReceptionistUpdate
from typing import List
from fastapi import HTTPException

router = APIRouter(prefix="/appointments", tags=["Appointment"])
manager = Manager()

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def add_appointment(new_appointment:AppointmentCreate,db:Session = Depends(get_db)):
    return manager.createappointment(new_appointment, db)

@router.get("/", response_model=List[AppointmentResponse], status_code=status.HTTP_200_OK)
def get_appointments(db:Session = Depends(get_db)):
    appointments = manager.view_appointments(db)
    return appointments or []

@router.get("/{appointment_id}", response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
def get_appointments_byid(appointment_id ,db:Session = Depends(get_db)):
    appointment = manager.get_appointments_by_id(db,appointment_id)
    if appointment is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Appointment with id {appointment_id} not found")
    return appointment 

@router.patch("/{appointment_id}",response_model=ReceptionistResponse, status_code=status.HTTP_201_CREATED)
def update_patient_appointments(appointment_id:int,appointment_in:ReceptionistUpdate,db:Session = Depends(get_db)):
    update_appointment = manager.update_patch_appointments(db,appointment_id,appointment_in)
    if not update_appointment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Appointment with id {appointment_id} not found")
    manager.schedule_appointment_status(db,appointment_id)
    
    return update_appointment
    

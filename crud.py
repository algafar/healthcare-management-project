from sqlalchemy.orm import Session 
from schemas import DoctorCreate
from model import Doctor
from sqlalchemy import select

def createdoctor(doctor:DoctorCreate,session: Session ):
    db_doctor = Doctor(**doctor.model_dump())
    session.add(db_doctor)
    session.commit()
    session.refresh(db_doctor)
    return db_doctor

def view_doctors(session:Session):
    return session.scalars(select(Doctor)).all()


from schemas import UserCreate,UserResponse
from model import Users
from fastapi import APIRouter,status,Depends,HTTPException
from crud import Manager
from sqlalchemy.orm import Session
from OAUTH.security import hashed_password
from app.database import get_db

router = APIRouter(prefix="/Users",tags=["Users"])
manager = Manager()

@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def usercreate(new_user:UserCreate,db:Session = Depends(get_db)):
    doctor = manager.get_doctors_by_email(new_user.email,db)
    patient = manager.get_patient_by_email(new_user.email,db)
    

    if not doctor and patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="email not registered"
        ) 
    hash_password = hashed_password(new_user.password)
    if doctor:
        try:
            doctors = Users(doctor.email,doctor.role,hash_password)
            db.add(doctors)
            db.commit()  
            db.refresh(doctors)
            return doctors
        except Exception as e:
            db.rollback()
            raise e
    if patient:
        try:
            patients = Users(patient.email,patient.role,hash_password)
            db.add(patients)
            db.commit()
            db.refresh(patients)
            return patients
        except Exception as e:
            db.rollback()
            raise e
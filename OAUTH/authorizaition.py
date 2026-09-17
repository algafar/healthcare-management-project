from OAUTH.dependencies import get_current_user
from model import Patient,Doctor
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from model import Role


def require_patient(current_user: Patient = Depends(get_current_user),db:Session = Depends(get_db)):
    if current_user.role != Role.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail="Patient access required"
        )
    return current_user

def require_doctor(current_user: Doctor = Depends(get_current_user),db:Session = Depends(get_db)):
    if current_user.role != Role.DOCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Doctor access required"
        )
    return current_user

def require_admin(current_user):
    return current_user
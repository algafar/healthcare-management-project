from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import DoctorCreate,DoctorResponse


router = APIRouter(prefix="/doctors", tags=["Doctors"])
manager = Manager()

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def add_doctor(new_doctor:DoctorCreate,db:Session = Depends(get_db)):
    return manager.createdoctor(new_doctor, db)
 
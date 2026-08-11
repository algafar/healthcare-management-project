from fastapi import FastAPI,Depends
from app.database import engine, Base, get_db
from model import Doctor
from crud import createdoctor, view_doctors
from sqlalchemy.orm import Session
from schemas import DoctorCreate,DoctorResponse


Base.metadata.create_all(engine)
app = FastAPI()


@app.post('/doctor/', response_model= DoctorResponse )
def add_doctor(new_doctor:DoctorCreate,db:Session = Depends(get_db)):
    return createdoctor(session=db,doctor = new_doctor)
 
@app.get('/doctors/',response_model= list[DoctorResponse])
def get_doctors(db:Session = Depends(get_db)):
    return view_doctors(session=db)


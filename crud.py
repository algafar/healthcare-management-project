from sqlalchemy.orm import Session
from schemas import (DoctorCreate,PatientCreate,AppointmentCreate,InvoiceCreate,MedicalRecordCreate,PaymentCreate,SpecialtiesCreate,ReceptionistUpdate)
from model import (Doctor,Patient,Appointment,Invoice,MedicalRecord,Payment,Specialty)
from sqlalchemy import select,func, update
from fastapi import HTTPException,status
from typing import List
from datetime import datetime,timedelta

class Manager:
    #Doctor
    def createdoctor(self,doctor:DoctorCreate,session: Session ):
        db_doctor = Doctor(**doctor.model_dump())
        session.add(db_doctor)
        session.commit()
        session.refresh(db_doctor)
        return db_doctor

    def view_doctors(self,session:Session):
        return session.scalars(select(Doctor)).all()

    def get_doctor_by_id(self,session:Session,doctor_id: int):
        return session.scalar(select(Doctor).where(Doctor.doctor_id == doctor_id))

    def delete_doctor(self,session:Session, doctor_id:int):
        return session.delete(select(Doctor).where(Doctor.doctor_id == doctor_id))

    def search_doctors_appointment(self,session:Session,specialty_id:int,duty:str):
        stmt = (
            select(Doctor.doctor_id, func.count(Appointment.appointment_id).label("total_appointments"))
            .join(Appointment,Doctor.doctor_id == Appointment.doctor_id).where(Doctor.specialty_id==specialty_id,Doctor.duty==duty).group_by(Doctor.doctor_id)
        )
        results = session.execute(stmt).all()
        return results
    #Patient
    def createpatient(self,patient:PatientCreate, session:Session):
        db_patient = Patient(**patient.model_dump())
        session.add(db_patient)
        session.commit()
        session.refresh(db_patient)
        return db_patient

    def view_patients(self,session:Session):
        return session.scalars(select(Patient)).all()

    def get_patient_by_id(self,session:Session,id: int):
        return session.scalar(select(Patient).where(Patient.id == id))

    #Appointment
    def createappointment(self,appointment:AppointmentCreate, session:Session):
        db_appointment = Appointment(**appointment.model_dump())
        session.add(db_appointment)
        session.commit()
        session.refresh(db_appointment)
        return db_appointment

    def view_appointments(self,session:Session):
        return session.scalars(select(Appointment)).all()

    def appointment(self,session:Session,appointment_id):
        return session.scalars(select(Appointment).where(Appointment.appointment_id==appointment_id)).first()
    
    def get_appointments_by_id(self,session:Session,appointment_id: int):
        return session.scalar(select(Appointment).where(Appointment.appointment_id == appointment_id))

    def update_patch_appointments(self,session:Session, appointment_id: int, appointment_in:ReceptionistUpdate):
        db_appointment = session.scalars(select(Appointment).where(Appointment.appointment_id==appointment_id)).first()
        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found"
            )
        update_data = appointment_in.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found"
            )
        for key,value in update_data.items():
            setattr(db_appointment,key,value)
            session.add(db_appointment)
            session.commit()
            session.refresh(db_appointment)
        
        
        return db_appointment

    def select_patient_with_appointment(self,session: Session, patient_id,status = "scheduled"):
        appointment_id = session.scalars(select(Appointment.appointment_date).where(Appointment.patient_id==patient_id,Appointment.status == status))
        return appointment_id

    def get_invoice_by_appointment(self,session:Session,appointment_id):
        return session.scalar(select(Invoice).where(Invoice.appointment_id == appointment_id))

    def schedule_appointment_status(self,session:Session,appointment_id):
        stmt = (
            update(Appointment).where(Appointment.appointment_id == appointment_id).values(status="scheduled")
        )
        session.execute(stmt)
        session.commit()
    
    def complete_appointment_status(self,session:Session,appointment_id):
            stmt = (
                update(Appointment).where(Appointment.appointment_id == appointment_id).values(status="completed")
            )
            session.execute(stmt)
            session.commit()
        
                
    def calculate_available_15_minutes(self,doctor_id:int,date_str:str,session:Session,work_hour: int =9,end_hour: int =15)-> List[datetime]:
        #generate timestamp based on work period 
        day = datetime.strptime(date_str, "%Y-%m-%d")
        work_start = day.replace(hour=work_hour, minute=0, second=0)
        work_end = day.replace(hour=end_hour, minute=0, second=0)
        # generate all potential 15 minutes slot
        all_possible_slots = []
        current_time = work_start
        while current_time < work_end:
            all_possible_slots.append(current_time)
            current_time += timedelta(minutes=15)
        books_slot_query = select(Appointment.appointment_date).where(Appointment.doctor_id==doctor_id,Appointment.appointment_date>=work_start,Appointment.appointment_date<work_end,)
        books_slot = set(session.scalars(books_slot_query).all())
        open_slots = [slot for slot in all_possible_slots if slot not in books_slot]
        return open_slots


    #Medicalrecord
    def create_medicalrecord(self,medicalrecord:MedicalRecordCreate, session:Session):
        session.add(medicalrecord)
        session.commit()
        session.refresh(medicalrecord)
        return medicalrecord

    def view_medicalrecord(self,session:Session):
        return session.scalars(select(MedicalRecord)).all()

    def get_medicalrecord_by_id(self,session:Session,record_id: int):
        return session.scalar(select(MedicalRecord).where(MedicalRecord.record_id == record_id))

    #invoices
    def create_invoices(self,invoice:InvoiceCreate, session:Session):
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return invoice

    def view_invoice(self,session:Session):
        return session.scalars(select(MedicalRecord)).all()

    def get_invoice_by_id(self,session:Session,invoice_id: int):
        return session.scalar(select(Invoice).where(Invoice.invoice_id== invoice_id))



    #Specialties
    def create_specialty(self,specialty:Specialty, session:Session):
        db_specialty = Specialty(**specialty.model_dump())
        session.add(db_specialty)
        session.commit()
        session.refresh(db_specialty)
        return db_specialty

    def view_specialty(self,session:Session):
        return session.scalars(select(Specialty)).all()

    def get_specialty_by_id(self,session:Session,id: int):
        return session.scalar(select(Specialty).where(Specialty.id == id))

    #payments
    def create_payment(self,payment:PaymentCreate, session:Session):
        db_payment = Payment(**payment.model_dump())
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)
        return db_payment

    def view_payments(self,session:Session):
        return session.scalars(select(Payment)).all()

    def get_payment_by_id(self,session:Session,payment_id: int):
        return session.scalar(select(Payment).where(Payment.payment_id == payment_id))

    

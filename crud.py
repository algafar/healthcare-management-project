from sqlalchemy.orm import Session 
from schemas import (DoctorCreate,PatientCreate,AppointmentCreate,InvoiceCreate,MedicalRecordCreate,PaymentCreate,SpecialtiesCreate)
from model import (Doctor,Patient,Appointment,Invoice,MedicalRecord,Payment,Specialty)
from sqlalchemy import select

class Manager:
    #Doctor
    def createdoctor(self,doctor:DoctorCreate,session: Session ):
        db_doctor = Doctor(**doctor.model_dump())
        session.add(db_doctor)
        session.commit()
        session.refresh(db_doctor)
        return db_doctor

    def view_doctors(session:Session):
        return session.scalars(select(Doctor)).all()

    def get_doctor_by_id(session:Session,doctor_id: int):
        return session.scalar(select(Doctor)).where(Doctor.doctor_id == doctor_id)

    #Patient
    def createpatient(patient:PatientCreate, session:Session):
        db_patient = Patient(**patient.model_dump())
        session.add(db_patient)
        session.commit()
        session.refresh(db_patient)
        return db_patient

    def view_patients(session:Session):
        return session.scalars(select(Patient)).all()

    def get_patient_by_id(session:Session,patient_id: int):
        return session.scalar(select(Patient)).where(Patient.patient_id == patient_id)

    #Appointment
    def createappointment(appointment:AppointmentCreate, session:Session):
        db_appointment = Appointment(**appointment.model_dump())
        session.add(db_appointment)
        session.commit()
        session.refresh(db_appointment)
        return db_appointment

    def view_appointments(session:Session):
        return session.scalars(select(Appointment)).all()

    def get_appointments_by_id(session:Session,appointment_id: int):
        return session.scalar(select(Appointment)).where(Appointment.appointment_id == appointment_id)

    #Medicalrecord
    def create_medicalrecord(medicalrecord:MedicalRecordCreate, session:Session):
        db_medicalrecord = Patient(**medicalrecord.model_dump())
        session.add(db_medicalrecord)
        session.commit()
        session.refresh(db_medicalrecord)
        return db_medicalrecord

    def view_medicalrecord(session:Session):
        return session.scalars(select(MedicalRecord)).all()

    def get_medicalrecord_by_id(session:Session,record_id: int):
        return session.scalar(select(MedicalRecord)).where(MedicalRecord.record_id == record_id)

    #invoices
    def create_invoices(invoice:InvoiceCreate, session:Session):
        db_invoice = Invoice(**invoice.model_dump())
        session.add(db_invoice)
        session.commit()
        session.refresh(db_invoice)
        return db_invoice

    def view_invoice(session:Session):
        return session.scalars(select(MedicalRecord)).all()

    def get_invoice_by_id(session:Session,invoice_id: int):
        return session.scalar(select(Invoice)).where(Invoice.invoice_id== invoice_id)

    #Specialties
    def create_specialty(specialty:Specialty, session:Session):
        db_specialty = Specialty(**specialty.model_dump())
        session.add(db_specialty)
        session.commit()
        session.refresh(db_specialty)
        return db_specialty

    def view_specialty(session:Session):
        return session.scalars(select(Specialty)).all()

    def get_specialty_by_id(session:Session,id: int):
        return session.scalar(select(Specialty)).where(Specialty.id == id)


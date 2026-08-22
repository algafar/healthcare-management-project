from decimal import Decimal
from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import date,datetime

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    specialty_id: int
    role: str
    duty: str
class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doctor_id: int
    first_name: str
    last_name: str  
    phone_number: str
    email: str
    specialty_id: int
    role: str
    duty: str

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    dob: date
    address: str
    email: EmailStr
    phone_number: str
    gender: str
    role: str

class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class AppointmentCreate(BaseModel):
    patient_id: int
    reasons: str
    requested_date: date
    

class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str

class InvoiceCreate(BaseModel):
    patient_id: int
    appointment_id: int
    total_amount: Decimal
    status: str
    date: date

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    patient_id: int
    appointment_id: int
    total_amount: Decimal
    status: str
    date: date

class MedicalRecordCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_id: int
    symptoms: str
    diagnosis: str
    prescription: str
    date: date

class MedicalRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    doctor_id: int
    patient_id: int
    appointment_id: int
    symptoms: str
    diagnosis: str
    prescription: str
    date: date

class PaymentCreate(BaseModel):
    invoice_id: int
    amount: Decimal
    date: date

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    invoice_id: int
    amount: Decimal
    date: date

class SpecialtiesCreate(BaseModel):
    specialty: str

class SpecialtiesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    specialty: str






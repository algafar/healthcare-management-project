from decimal import Decimal
from pydantic import BaseModel,ConfigDict,EmailStr,field_validator
from datetime import date,datetime,timedelta
from typing import Optional,List


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
    id: int
    first_name: str
    last_name: str
    dob: date
    address: str
    email: EmailStr
    phone_number: str
    gender: str
    role: str

class AppointmentCreate(BaseModel):
    patient_id: int
    reasons: str
    requested_date: date
    

class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    appointment_id: int
    patient_id: int
    reasons: str
    requested_date: date
    status: str
    date: datetime

class Available_slotResponse(BaseModel):
    doctor_id: int
    date: str
    available_slots: List[datetime]

class InvoiceCreate(BaseModel):
    patient_id: int
    appointment_id: int
    total_amount: Decimal
    

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    invoice_id: int
    patient_id: int
    appointment_id: int
    total_amount: Decimal
    status: str
    date: datetime

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
    

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    payment_id: int
    invoice_id: int
    amount: Decimal
    date: datetime

class SpecialtiesCreate(BaseModel):
    specialty: str

class SpecialtiesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    specialty: str

class ReceptionistUpdate(BaseModel):
    doctor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None

    @field_validator("appointment_date")
    @classmethod
    def validate_15min_step_away(cls, value:datetime)-> datetime:
        if value.minute not in (0,15,30,45) or value.second != 0:
            raise ValueError("appointment must start on 15- minutes intervals (eg. 9:00, 9:15, 9:30, 9:45)")
        return value

    @field_validator("appointment_date")
    @classmethod
    def validate_current_work_week(cls, value:datetime)-> datetime:
        now = datetime.now()
        current_monday = (now - timedelta(days = now.weekday())).replace(hour=0,minute=0,second=0,microsecond=0)
        current_friday_end = current_monday + timedelta(days=4,hours=23,minutes=59,seconds=59)
        if not (current_monday <= value <= current_friday_end):
            raise ValueError("Appointment can only booked for the current week(Monday to friday).")
        if value.weekday > 4:
            raise ValueError("Appointment cannot be booked on weekends")
        return value
    
    @field_validator("appointment_date")
    @classmethod
    def prevent_past_date(cls, value:datetime)-> datetime:
        now = datetime.now()
        if value < now:
            raise ValueError("Appointment cannot be book with past date")
        return value
    
class ReceptionistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    appointment_id: int
    patient_id: int
    doctor_id: Optional[int]= None
    reasons: str
    requested_date: date
    appointment_date: Optional[datetime] = None
    date: datetime
    status: str

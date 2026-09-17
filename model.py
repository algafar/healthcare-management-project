from datetime import datetime,timezone,date
from sqlalchemy import DateTime,func,Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,ForeignKey,Integer,Text
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum,UniqueConstraint,CheckConstraint
from sqlalchemy import Numeric


class SpecialtyType(str,PyEnum):
    CARDIOLOGY = "cardiology"
    ORTHOPEDICS = "orthopedics"
    PSYCHIATRIC = "psychiatric"
    DERMATOLOGY = "dermatology"
    GYNECOLOGY = "gynecology"
    DENTIST = "dentist"
    NEOROLOGY = "neorology"

class Status(str, PyEnum):
    SCHDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    PENDING = "pending"

class Role(str, PyEnum):
    ADMIN = "admin"
    DOCTOR= "doctor"
    PATIENT = "patient"

class Duty(str, PyEnum):
    OFF_DUTY = "off_duty"
    ACTIVE = "active"

class Gender(str, PyEnum):
    MALE = "male"
    FEMALE = "female"

class PaymentStatus(str, PyEnum):
    PAID = "paid"
    PENDING = "pending"

class Doctor(Base): 
    __tablename__ = "doctors"

    doctor_id: Mapped[int] = mapped_column(Integer,primary_key = True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number:Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email:Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    specialty_id:Mapped[int] = mapped_column(ForeignKey("specialties.id"), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False), default= Role.DOCTOR)
    duty: Mapped[Duty] = mapped_column(Enum(Duty, native_enum=False),nullable=True, default=Duty.OFF_DUTY)

    specialties: Mapped["Specialty"] = relationship(
        back_populates="doctors"
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctors"
    )
    medicalrecords:  Mapped[list["MedicalRecord"]] = relationship(
        back_populates="doctors"
    )

class Specialty(Base):
    __tablename__ = "specialties"

    id:Mapped[int] = mapped_column(primary_key=True)
    specialty:Mapped[SpecialtyType] = mapped_column(
        Enum(SpecialtyType), nullable=False
    )
    doctors:Mapped[list["Doctor"]] = relationship(
        back_populates="specialties"
    )

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    dob: Mapped[date]= mapped_column(Date)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False), default= Role.PATIENT)

    medicalrecords: Mapped[list["MedicalRecord"]] = relationship(
        back_populates="patients"
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patients"
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="patients"
    )

class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"))
    reasons: Mapped[str] = mapped_column(Text, nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.doctor_id"),nullable=True)
    appointment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default=Status.PENDING)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__= (
        UniqueConstraint("doctor_id","appointment_date",name="uq_doctor_appointment_date"),
    )

    patients: Mapped["Patient"] = relationship(
        back_populates="appointments"
    ) 
    doctors: Mapped["Doctor"] = relationship(
        back_populates="appointments"
    )
    
    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="appointments"
    )
    medicalrecords: Mapped["MedicalRecord"] = relationship(
        back_populates="appointments"
    )


class MedicalRecord(Base):
    __tablename__ = "medicalrecords"
    record_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.doctor_id"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.appointment_id"))
    symptoms: Mapped[str] = mapped_column(Text, nullable= False)
    diagnosis: Mapped[str] = mapped_column(String(200), nullable=False)
    prescription: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    doctors: Mapped["Doctor"] = relationship(
        back_populates="medicalrecords"
    )
    patients: Mapped["Patient"] = relationship(
        back_populates="medicalrecords"
    )
    appointments: Mapped["Appointment"] = relationship(
        back_populates="medicalrecords"
    )
class Invoice(Base):
    __tablename__ = "invoices"
    invoice_id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.appointment_id"), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus, native_enum=False), default=PaymentStatus.PENDING)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) 

    __table_args__ = (
        UniqueConstraint("appointment_id", name="uq_invoices_appointment_id"),
        CheckConstraint("total_amount > 0", name="check_positive_invoice_amount"),
    )

    patients: Mapped["Patient"] = relationship(
        back_populates="invoices"
    )
    appointments: Mapped["Appointment"] = relationship(
        back_populates="invoices"
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="invoices"
    )
class Payment(Base):
    __tablename__ = "payments"
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"))
    amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    invoices: Mapped["Invoice"] = relationship(
        back_populates="payments"
    )

class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role),native_enum=False, nullable=False)
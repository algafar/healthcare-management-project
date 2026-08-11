from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,Integer,ForeignKey,Date,DateTime, Text 
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    age:Mapped[int]

    patients: Mapped[list["Patient"]] = relationship(
        back_populates="doctor"
    )

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.doctor_id"))
    doctor: Mapped["Doctor"] = relationship(
        back_populates="patients"
    )
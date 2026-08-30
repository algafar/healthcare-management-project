from fastapi import FastAPI
from app.database import engine, Base
from routers.doctors import router as doctors_router
from routers.specialty import router as specialty_router
from routers.patients import router as patients_router
from routers.appointment import router as appointments_router
from routers.medicalrecord import router as medicalrecord_router
from routers.payments import router as payment_router
from routers.invoice import router as invoice_router




Base.metadata.create_all(engine)
app = FastAPI(title="Healthcare Management System")
app.include_router(doctors_router)
app.include_router(specialty_router)
app.include_router(patients_router)
app.include_router(appointments_router)
app.include_router(medicalrecord_router)
app.include_router(invoice_router)
app.include_router(payment_router)




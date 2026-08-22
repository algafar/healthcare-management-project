from fastapi import FastAPI
from app.database import engine, Base
from routers.doctors import router as doctors_router


Base.metadata.create_all(engine)
app = FastAPI(title="Healthcare Management System")
app.include_router(doctors_router)




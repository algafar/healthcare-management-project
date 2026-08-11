from pydantic import BaseModel,ConfigDict

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    age: int

class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doctor_id: int
    first_name: str
    last_name: str  
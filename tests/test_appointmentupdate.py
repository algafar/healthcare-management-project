from model import Doctor,Specialty,Patient,Appointment
async def test_update_appointments(client,db_session):
    specialties = [
        Specialty(specialty="orthopedics"),
        Specialty(specialty="cardiology"),
        Specialty(specialty="neorology"),
    ]
    db_session.add_all(specialties)
    db_session.flush()
    
    doctors =[
        Doctor(first_name = "Yusuf",last_name= "Gafar",phone_number= "09063222257",email= "amina@example.com",specialty_id=specialties[0].id,role="doctor",duty="off_duty"),
        Doctor(first_name = "imam",last_name= "rahman",phone_number= "09063222254",email= "amia@example.com",specialty_id=specialties[1].id,role="doctor",duty="off_duty"),
        Doctor(first_name = "Yiza",last_name= "jeff",phone_number= "09063222253",email= "aina@example.com",specialty_id=specialties[2].id,role="doctor",duty="active"),
    ]
   
    db_session.add_all(doctors)
    db_session.flush()
    print(doctors[0].doctor_id)
    
    patients =[
        Patient(first_name = "Yusuf",last_name= "Gafar",dob="2026-08-21",address="osoma street",email= "ina@example.com",phone_number= "09063222257",
                       gender= "male",role= "patient"),
        Patient(first_name = "Yhaf",last_name= "habib",dob="2026-08-21",address="osoma street",email= "na@example.com",phone_number= "09063222256",
                       gender= "female",role= "patient")
    ]
    db_session.add_all(patients)
    db_session.flush()
    appointments = Appointment(patient_id = patients[1].id,reasons= "headeache",requested_date= "2026-08-20")
    db_session.add(appointments)
    db_session.flush()
    db_session.refresh(appointments) 
    payload = {
        "doctor_id": doctors[1].doctor_id,
        "appointment_date": "2026-09-01T14:30:00"
    }
    response = await client.patch(f'/appointments/{appointments.appointment_id}',json=payload)    
    assert response.status_code==201
    data = response.json()
    assert data["doctor_id"]== doctors[1].doctor_id
    assert data["appointment_date"]== "2026-09-01T14:30:00"
    
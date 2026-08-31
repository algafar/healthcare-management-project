from model import Patient,Doctor,Appointment,Specialty
async def test_create_invoice(client,db_session):
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
    
    
    patients =[
        Patient(first_name = "Yusuf",last_name= "Gafar",dob="2026-08-21",address="osoma street",email= "ina@example.com",phone_number= "09063222257",
                       gender= "male",role= "patient"),
        Patient(first_name = "Yhaf",last_name= "habib",dob="2026-08-21",address="osoma street",email= "na@example.com",phone_number= "09063222256",
                       gender= "female",role= "patient")
    ]
    db_session.add_all(patients)
    db_session.flush()
    appointments = [
        Appointment(doctor_id=doctors[1].doctor_id,patient_id=patients[0].id,appointment_date="2026-08-21T14:30:00",date="2026-08-20",status= "scheduled",reasons= "headeache",
                       requested_date= "2026-08-20"),
        
        Appointment(doctor_id=doctors[0].doctor_id,patient_id=patients[1].id,appointment_date="2026-08-21T13:30:00",date="2026-08-20",status= "completed",reasons= "neck",
                       requested_date= "2026-08-20")
    ] 
    db_session.add_all(appointments)
    db_session.flush()
    payload = {
        "patient_id": appointments[1].patient_id,
        "appointment_id": appointments[1].appointment_id,
        "total_amount": "2000.00"
    }
    response = await client.post("/invoices/", json=payload)
    print(response.json())
    assert response.status_code==201
    data = response.json()
    assert data["patient_id"] == appointments[1].patient_id
    assert data["appointment_id"]== appointments[1].appointment_id
    assert data["total_amount"] == "2000.00"
    
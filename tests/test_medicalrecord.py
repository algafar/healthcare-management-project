from model import Patient,Doctor,Appointment,Specialty
async def test_create_medicalrecord(client,db_session):
    specialty = Specialty(specialty="Cardiology")
    db_session.add(specialty)
    db_session.flush()
    db_session.refresh(specialty)
    patients = Patient(first_name = "Yusuf",last_name= "Gafar",dob="2026-08-21",address="osoma street",email= "amina@example.com",phone_number= "09063222257",
                       gender= "male",role= "patient")
    db_session.add(patients)
    db_session.flush()
    db_session.refresh(patients)

    doctors = Doctor(first_name = "Yusuf",last_name= "Gafar",phone_number= "09063222259",email= "amina@example.com",specialty_id= specialty.id,role="doctor",duty="off_duty")
    db_session.add(doctors)
    db_session.flush()
    db_session.refresh(doctors) 
    appointments = Appointment(doctor_id=doctors.doctor_id,patient_id=patients.id,appointment_date="2026-08-21T14:30:00",date="2026-08-20",status= "scheduled",reasons= "headeache",
                       requested_date= "2026-08-20")
    db_session.add(appointments)
    db_session.flush()
    db_session.refresh(appointments) 
    payload = {
        "doctor_id": appointments.doctor_id,
        "patient_id": appointments.patient_id,
        "appointment_id": appointments.appointment_id,
        "symptoms": "headache",
        "diagnosis": "migrane",
        "prescription": "paracetamol",
        
    }
    response = await client.post("/medicalrecords/", json=payload)
    assert response.status_code==201
    data = response.json()
    print(appointments.status)
    assert data["doctor_id"] ==appointments.doctor_id
    assert data["patient_id"] ==appointments.patient_id
    assert data["appointment_id"] ==appointments.appointment_id
    assert data["symptoms"] =="headache"
    assert data["diagnosis"] =="migrane"
    assert data["prescription"] =="paracetamol"
    

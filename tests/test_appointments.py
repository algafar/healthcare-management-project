from model import Patient
async def test_create_appointments(client,db_session):
    patients = Patient(first_name = "Yusuf",last_name= "Gafar",dob="2026-08-21",address="osoma street",email= "amina@example.com",phone_number= "09063222257",
                       gender= "male",role= "patient")
    db_session.add(patients)
    db_session.flush()
    db_session.refresh(patients)
    payload = {
        "patient_id": patients.id,
        "reasons": "headache",
        "requested_date": "2026-08-28"
    }
    response = await client.post("/appointments/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["patient_id"] == patients.id
    assert data["reasons"] == "headache"
    assert data["requested_date"] == "2026-08-28"
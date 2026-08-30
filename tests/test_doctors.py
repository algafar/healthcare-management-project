from model import Specialty
from schemas import DoctorResponse

async def test_create_doctor(client, db_session):
    specialty = Specialty(specialty="Cardiology")
    db_session.add(specialty)
    db_session.flush()
    db_session.refresh(specialty)
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "phone_number": "09063222257",
            "email": "amina@example.com",
            "specialty_id": specialty.id,
            "role": "doctor",
            "duty": "off_duty"
        }
    response = await client.post(
        "/doctors/",
        json=payload
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Yusuf"
    assert data["last_name"] == "Gafar"
    assert data["phone_number"] == "09063222257"
    assert data["email"] == "amina@example.com"
    assert data["specialty_id"] == specialty.id
    assert data["role"] == "doctor"
    assert data["duty"] == "off_duty"
    assert "doctor_id" in data


async def test_view_doctors(client, db_session):
    specialty = Specialty(specialty="Cardiology")
    db_session.add(specialty)
    db_session.flush()
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "phone_number": "09063222257",
            "email": "amina@example.com",
            "specialty_id": specialty.id,
            "role": "doctor",
            "duty": "off_duty"
        }
    create_res = await client.post(
        "/doctors/",
        json=payload
    )
    assert create_res.status_code==201
    response = await client.get("/doctors/")
    assert response.status_code==200
    data = response.json()
    assert isinstance(data, list)
    doctors = [DoctorResponse(**doctor) for doctor in data]
    assert len(doctors) >= 1

async def test_get_doctor_byid(client, db_session):
    specialty = Specialty(specialty="Cardiology")
    db_session.add(specialty)
    db_session.flush()
    db_session.refresh(specialty)
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "phone_number": "09063222257",
            "email": "amina@example.com",
            "specialty_id": specialty.id,
            "role": "doctor",
            "duty": "off_duty"
        }
    create_res = await client.post(
        "/doctors/",
        json=payload
    )
    assert create_res.status_code==201
    doctor_id = create_res.json()['doctor_id']
    response = await client.get(f'/doctors/{doctor_id}')
    assert response.status_code==200
    data = response.json()
    assert len(data) >= 1
    assert data["email"]== "amina@example.com"


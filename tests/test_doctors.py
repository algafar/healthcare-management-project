from model import Specialty
import pytest


async def test_create_doctor(client, db_session):
    specialty = Specialty(id=2, specialty="Cardiology")
    db_session.add(specialty)
    db_session.commit()
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "phone_number": "09063222257",
            "email": "amina@example.com",
            "specialty_id": 2,
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
    assert data["specialty_id"] == 2
    assert data["role"] == "doctor"
    assert data["duty"] == "off_duty"
    assert "doctor_id" in data


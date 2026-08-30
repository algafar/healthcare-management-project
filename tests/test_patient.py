from schemas import PatientResponse

async def test_create_patient(client):
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "dob": "2026-08-21",
            "address": "osoma street",
            "email": "amina@example.com",
            "phone_number": "09063222257",
            "gender": "male",
            "role": "patient",
        }
    response = await client.post(
        "/patients/",
        json=payload
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Yusuf"
    assert data["last_name"] == "Gafar"
    assert data["dob"] == "2026-08-21"
    assert data["address"] == "osoma street"
    assert data["email"] == "amina@example.com"
    assert data["phone_number"] == "09063222257"
    assert data["gender"] == "male"
    assert data["role"] == "patient"
    assert "id" in data


async def test_view_patients(client):
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "dob": "2026-08-21",
            "address": "osoma street",
            "email": "amina@example.com",
            "phone_number": "09063222257",
            "gender": "male",
            "role": "patient",
        } 
    create_res = await client.post(
        "/patients/",
        json=payload
    )
    assert create_res.status_code==201
    response = await client.get("/patients/")
    assert response.status_code==200
    data = response.json()
    assert isinstance(data, list)
    patients = [PatientResponse(**patient) for patient in data]
    assert len(patients) >= 1

async def test_get_patient_byid(client):
    payload= {
            "first_name": "Yusuf",
            "last_name": "Gafar",
            "dob": "2026-08-21",
            "address": "osoma street",
            "email": "amina@example.com",
            "phone_number": "09063222257",
            "gender": "male",
            "role": "patient",
        }
    create_res = await client.post(
        "/patients/",
        json=payload
    )
    assert create_res.status_code==201
    id = create_res.json()['id']
    response = await client.get(f'/patients/{id}')
    assert response.status_code==200
    data = response.json()
    assert len(data) >= 1
    assert data["email"]== "amina@example.com"
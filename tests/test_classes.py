
def test_create_class_requires_auth(client):
    response = client.post(
        "/classes",
        json={
            "name": "Yoga Flow",
            "dateTime": "2026-12-01T10:00:00+05:30",
            "instructor": "John Doe",
            "availableSlots": 10,
        },
    )
    assert response.status_code == 401

def test_create_class_success(client, auth_headers):
    response = client.post(
        "/classes",
        headers=auth_headers,
        json={
            "name": "Yoga Flow",
            "dateTime": "2026-12-01T10:00:00+05:30",
            "instructor": "John Doe",
            "availableSlots": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Yoga Flow"
    assert data["instructor"] == "John Doe"
    assert data["availableSlots"] == 10
    assert "id" in data

def test_create_class_missing_field_fails(client, auth_headers):
    response = client.post(
        "/classes",
        headers=auth_headers,
        json={"name": "Incomplete Class"},
    )
    assert response.status_code == 422

def test_create_class_without_timezone_fails(client, auth_headers):

    response = client.post(
        "/classes",
        headers=auth_headers,
        json={
            "name": "Bad Timezone Class",
            "dateTime": "2026-12-01T10:00:00",  # no tz offset
            "instructor": "John Doe",
            "availableSlots": 5,
        },
    )
    assert response.status_code == 422

def test_list_classes_is_public(client, auth_headers):

    client.post(
        "/classes",
        headers=auth_headers,
        json={
            "name": "HIIT Session",
            "dateTime": "2026-12-05T08:00:00+05:30",
            "instructor": "Jane Smith",
            "availableSlots": 15,
        },
    )

    response = client.get("/classes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(c["name"] == "HIIT Session" for c in data)

def test_list_classes_excludes_past_classes(client, auth_headers):
    client.post(
        "/classes",
        headers=auth_headers,
        json={
            "name": "Old Class",
            "dateTime": "2020-01-01T10:00:00+05:30",
            "instructor": "Someone",
            "availableSlots": 5,
        },
    )
    response = client.get("/classes")
    assert response.status_code == 200
    names = [c["name"] for c in response.json()]
    assert "Old Class" not in names
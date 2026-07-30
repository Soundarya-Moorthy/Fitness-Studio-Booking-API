
import pytest

@pytest.fixture
def created_class(client, auth_headers):

    response = client.post(
        "/classes",
        headers=auth_headers,
        json={
            "name": "Small Class",
            "dateTime": "2026-12-10T09:00:00+05:30",
            "instructor": "Coach X",
            "availableSlots": 2,
        },
    )
    return response.json()

def test_book_class_requires_auth(client, created_class):
    response = client.post(
        "/book",
        json={
            "class_id": created_class["id"],
            "client_name": "Alice",
            "client_email": "alice@example.com",
        },
    )
    assert response.status_code == 401

def test_book_class_success(client, auth_headers, created_class):
    response = client.post(
        "/book",
        headers=auth_headers,
        json={
            "class_id": created_class["id"],
            "client_name": "Alice",
            "client_email": "alice@example.com",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["class_id"] == created_class["id"]
    assert data["client_name"] == "Alice"

def test_book_nonexistent_class_fails(client, auth_headers):
    response = client.post(
        "/book",
        headers=auth_headers,
        json={
            "class_id": 9999,
            "client_name": "Alice",
            "client_email": "alice@example.com",
        },
    )
    assert response.status_code == 404

def test_overbooking_is_prevented(client, auth_headers, created_class):
  
    booking_payload = {
        "class_id": created_class["id"],
        "client_name": "Client",
        "client_email": "client@example.com",
    }

    first = client.post("/book", headers=auth_headers, json=booking_payload)
    assert first.status_code == 201

    second = client.post("/book", headers=auth_headers, json=booking_payload)
    assert second.status_code == 201

    third = client.post("/book", headers=auth_headers, json=booking_payload)
    assert third.status_code == 400
    assert "no available slots" in third.json()["detail"].lower()

def test_slots_decrement_after_booking(client, auth_headers, created_class):
    client.post(
        "/book",
        headers=auth_headers,
        json={
            "class_id": created_class["id"],
            "client_name": "Alice",
            "client_email": "alice@example.com",
        },
    )
    response = client.get("/classes")
    classes = response.json()
    booked_class = next(c for c in classes if c["id"] == created_class["id"])
    assert booked_class["availableSlots"] == created_class["availableSlots"] - 1

def test_get_bookings_requires_auth(client):
    response = client.get("/bookings")
    assert response.status_code == 401

def test_get_bookings_returns_own_bookings(client, auth_headers, created_class):
    client.post(
        "/book",
        headers=auth_headers,
        json={
            "class_id": created_class["id"],
            "client_name": "Alice",
            "client_email": "alice@example.com",
        },
    )
    response = client.get("/bookings", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["class_id"] == created_class["id"]
    assert data[0]["client_name"] == "Alice"
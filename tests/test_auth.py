
def test_signup_success(client, test_user_data):
    response = client.post("/signup", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_user_data["name"]
    assert data["email"] == test_user_data["email"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_signup_duplicate_email_fails(client, test_user_data):
    client.post("/signup", json=test_user_data)
    response = client.post("/signup", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_signup_missing_field_fails(client):
    response = client.post(
        "/signup",
        json={"name": "No Email User", "password": "somepass"},
    )
    assert response.status_code == 422

def test_login_success(client, test_user_data):
    client.post("/signup", json=test_user_data)
    response = client.post(
        "/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password_fails(client, test_user_data):
    client.post("/signup", json=test_user_data)
    response = client.post(
        "/login",
        json={"email": test_user_data["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401

def test_login_nonexistent_user_fails(client):
    response = client.post(
        "/login",
        json={"email": "doesnotexist@example.com", "password": "whatever"},
    )
    assert response.status_code == 401
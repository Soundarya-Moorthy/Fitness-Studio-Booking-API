
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
   
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():

    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user_data():

    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass123",
    }

@pytest.fixture
def auth_token(client, test_user_data):
   
    client.post("/signup", json=test_user_data)
    response = client.post(
        "/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"],
        },
    )
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Authorization header dict, ready to pass into requests."""
    return {"Authorization": f"Bearer {auth_token}"}
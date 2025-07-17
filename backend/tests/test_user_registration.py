import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.api.v1.user import get_db
from app.db.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_duplicate_email():
    # Register the first user
    response1 = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "mobile_number": "+8801234567890",
            "password": "Str0ngP@ssw0rd!",
            "user_type": "patient",
        },
    )
    assert response1.status_code == 200

    # Attempt to register a second user with the same email
    response2 = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Another User",
            "email": "test@example.com",
            "mobile_number": "+8801234567891",
            "password": "Str0ngP@ssw0rd!",
            "user_type": "patient",
        },
    )
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]


def test_register_duplicate_mobile_number():
    # Register the first user
    response1 = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Test User",
            "email": "test1@example.com",
            "mobile_number": "+8801234567890",
            "password": "Str0ngP@ssw0rd!",
            "user_type": "patient",
        },
    )
    assert response1.status_code == 200

    # Attempt to register a second user with the same mobile number
    response2 = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Another User",
            "email": "test2@example.com",
            "mobile_number": "+8801234567890",
            "password": "Str0ngP@ssw0rd!",
            "user_type": "patient",
        },
    )
    assert response2.status_code == 400
    assert "Mobile number already registered" in response2.json()["detail"]

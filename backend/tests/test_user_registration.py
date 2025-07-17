import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.api.v1.auth import get_db
from app.db.models.user import User
import os

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
    # Create a dummy image file
    with open("dummy_image.png", "w") as f:
        f.write("dummy image content")
    yield
    Base.metadata.drop_all(bind=engine)
    os.remove("dummy_image.png")


def test_register_duplicate_email():
    # Register the first user
    with open("dummy_image.png", "rb") as f:
        response1 = client.post(
            "/api/v1/auth/register",
            data={
                "full_name": "Test User",
                "email": "test@example.com",
                "mobile_number": "+8801234567890",
                "password": "Str0ngP@ssw0rd!",
                "user_type": "patient",
                "division": "Dhaka",
                "district": "Dhaka",
                "thana": "Dhanmondi"
            },
            files={"profile_image": ("dummy_image.png", f, "image/png")},
        )
    assert response1.status_code == 200

    # Attempt to register a second user with the same email
    with open("dummy_image.png", "rb") as f:
        response2 = client.post(
            "/api/v1/auth/register",
            data={
                "full_name": "Another User",
                "email": "test@example.com",
                "mobile_number": "+8801234567891",
                "password": "Str0ngP@ssw0rd!",
                "user_type": "patient",
                "division": "Dhaka",
                "district": "Dhaka",
                "thana": "Dhanmondi"
            },
            files={"profile_image": ("dummy_image.png", f, "image/png")},
        )
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]


def test_register_duplicate_mobile_number():
    # Register the first user
    with open("dummy_image.png", "rb") as f:
        response1 = client.post(
            "/api/v1/auth/register",
            data={
                "full_name": "Test User",
                "email": "test1@example.com",
                "mobile_number": "+8801234567890",
                "password": "Str0ngP@ssw0rd!",
                "user_type": "patient",
                "division": "Dhaka",
                "district": "Dhaka",
                "thana": "Dhanmondi"
            },
            files={"profile_image": ("dummy_image.png", f, "image/png")},
        )
    assert response1.status_code == 200

    # Attempt to register a second user with the same mobile number
    with open("dummy_image.png", "rb") as f:
        response2 = client.post(
            "/api/v1/auth/register",
            data={
                "full_name": "Another User",
                "email": "test2@example.com",
                "mobile_number": "+8801234567890",
                "password": "Str0ngP@ssw0rd!",
                "user_type": "patient",
                "division": "Dhaka",
                "district": "Dhaka",
                "thana": "Dhanmondi"
            },
            files={"profile_image": ("dummy_image.png", f, "image/png")},
        )
    assert response2.status_code == 400
    assert "Mobile number already registered" in response2.json()["detail"]

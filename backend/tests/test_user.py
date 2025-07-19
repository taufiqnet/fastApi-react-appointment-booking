import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.db.models.user import User
import os
import json

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

@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)

def test_register_user_without_profile_image(db_session):
    user_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "mobile_number": "+8801234567890",
        "password": "Password@123",
        "user_type": "patient",
    }
    response = client.post("/api/v1/users/register", data=json.dumps(user_data))
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "profile_image" not in data

    # Verify user in db
    user = db_session.query(User).filter(User.email == user_data["email"]).first()
    assert user is not None
    assert user.profile_image is None

def test_register_user_with_profile_image(db_session):
    user_data = {
        "full_name": "Test User 2",
        "email": "test2@example.com",
        "mobile_number": "+8801234567891",
        "password": "Password@123",
        "user_type": "patient",
    }

    # Create the tests directory if it doesn't exist
    os.makedirs("backend/tests", exist_ok=True)

    with open("backend/tests/test_image.png", "wb") as f:
        f.write(b"test image data")

    with open("backend/tests/test_image.png", "rb") as f:
        response = client.post(
            "/api/v1/users/register",
            data={"user_data": json.dumps(user_data)},
            files={"profile_image": ("test_image.png", f, "image/png")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["profile_image"] is not None

    # Verify user in db
    user = db_session.query(User).filter(User.email == user_data["email"]).first()
    assert user is not None
    assert user.profile_image is not None

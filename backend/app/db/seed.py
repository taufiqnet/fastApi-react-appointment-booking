from app.db.database import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

def seed():
    db = SessionLocal()

    try:
        # Seed admin
        admin = User(
            full_name="Admin User",
            email="admin@example.com",
            mobile_number="+8801000000001",
            hashed_password=hash_password("Admin@123"),
            user_type="admin"
        )
        db.add(admin)

        # Seed doctor
        doctor = User(
            full_name="Dr. John",
            email="doctor@example.com",
            mobile_number="+8801000000002",
            hashed_password=hash_password("Doctor@123"),
            user_type="doctor",
            license_number="DOC-12345",
            experience_years=5,
            consultation_fee=500,
            available_timeslots="10:00-11:00,11:00-12:00"
        )
        db.add(doctor)

        # Seed patient
        patient = User(
            full_name="Patient One",
            email="patient@example.com",
            mobile_number="+8801000000003",
            hashed_password=hash_password("Patient@123"),
            user_type="patient"
        )
        db.add(patient)

        db.commit()
        print("✅ Seed data inserted successfully!")

    except IntegrityError:
        db.rollback()
        print("⚠️ Seed data already exists or duplicate detected.")

    finally:
        db.close()

if __name__ == "__main__":
    seed()

from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_mobile(db: Session, mobile_number: str):
    return db.query(User).filter(User.mobile_number == mobile_number).first()

def create_user(db: Session, user_data, image_data: bytes):
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        mobile_number=user_data.mobile_number,
        hashed_password=hash_password(user_data.password),
        user_type=user_data.user_type,
        division=user_data.division,
        district=user_data.district,
        thana=user_data.thana,
        profile_image=image_data,
        license_number=user_data.license_number,
        experience_years=user_data.experience_years,
        consultation_fee=user_data.consultation_fee,
        available_timeslots=user_data.available_timeslots
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

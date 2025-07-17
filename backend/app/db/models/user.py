from sqlalchemy import Column, String, Integer, Enum, Text, Float, LargeBinary
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.db.models.appointment import Appointment
import enum


class UserType(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    mobile_number = Column(String(14), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    # Address
    division = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    thana = Column(String(50), nullable=True)

    profile_image = Column(LargeBinary, nullable=True)

    # Doctor-specific fields
    license_number = Column(String(50), nullable=True)
    experience_years = Column(Integer, nullable=True)
    consultation_fee = Column(Float, nullable=True)
    available_timeslots = Column(Text, nullable=True)

    patient_appointments = relationship("Appointment", foreign_keys="Appointment.patient_id", back_populates="patient")
    doctor_appointments = relationship("Appointment", foreign_keys="Appointment.doctor_id", back_populates="doctor")

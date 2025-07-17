from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.db.database import Base

class AppointmentStatus(str, enum.Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    cancelled = "Cancelled"
    completed = "Completed"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    appointment_time = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)

    patient = relationship("User", foreign_keys=[patient_id], back_populates="patient_appointments")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="doctor_appointments")

from pydantic import BaseModel, Field, validator
from .user import UserBase
from typing import Literal, Optional
from datetime import datetime, timezone

class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_time: datetime
    notes: Optional[str] = None

    @validator("appointment_time")
    def not_in_past(cls, v):
        if v.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise ValueError("Appointment time cannot be in the past")
        return v

class AppointmentOut(BaseModel):  # ✅ Do NOT inherit from AppointmentCreate
    id: int
    patient_id: int
    doctor_id: int
    doctor: Optional[UserBase]
    patient: Optional[UserBase]
    appointment_time: datetime
    notes: Optional[str] = None
    status: Literal["Pending", "Confirmed", "Cancelled", "Completed"]

    class Config:
        orm_mode = True

class AppointmentStatusUpdate(BaseModel):
    status: Literal["Pending", "Confirmed", "Cancelled", "Completed"]

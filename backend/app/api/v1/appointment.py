from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, Literal
from datetime import date

from app.db.database import SessionLocal
from app.db.models.user import User
from app.db.models.appointment import Appointment
from app.db.schemas.appointment import AppointmentCreate, AppointmentOut, AppointmentStatusUpdate
from app.core.security import get_current_user
from app.tasks.report import generate_monthly_doctor_report

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------------------------------------
# Patient books an appointment
@router.post("/appointments", response_model=AppointmentOut)
def book_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != "patient":
        raise HTTPException(status_code=403, detail="Only patients can book appointments")

    doctor = db.query(User).filter(User.id == data.doctor_id, User.user_type == "doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if str(data.appointment_time.strftime("%H:%M")) not in doctor.available_timeslots:
        raise HTTPException(status_code=400, detail="Appointment time does not match doctor's availability")

    appointment = Appointment(
        patient_id=current_user.id,
        doctor_id=data.doctor_id,
        appointment_time=data.appointment_time,
        notes=data.notes
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

# ----------------------------------------------------------
# Doctor updates appointment status (e.g., Confirmed, Cancelled)
@router.patch("/appointments/{appointment_id}/status", response_model=AppointmentOut)
def update_appointment_status(
    appointment_id: int,
    data: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can update appointment status")

    appointment = db.query(Appointment).filter_by(id=appointment_id, doctor_id=current_user.id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found or not authorized")

    if appointment.status in ["Cancelled", "Completed"]:
        raise HTTPException(status_code=400, detail=f"Cannot update a {appointment.status.lower()} appointment")

    appointment.status = data.status
    db.commit()
    db.refresh(appointment)
    return appointment

# ----------------------------------------------------------
# NEW: Get appointments list (based on user type)
@router.get("/appointments", response_model=List[AppointmentOut])
def list_appointments(
    status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    doctor_name: Optional[str] = Query(None),  # New parameter for doctor name search
    patient_name: Optional[str] = Query(None),  # New parameter for patient name search
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Appointment)

    # Filtering by user role
    if current_user.user_type == "doctor":
        query = query.filter(Appointment.doctor_id == current_user.id)
    elif current_user.user_type == "patient":
        query = query.filter(Appointment.patient_id == current_user.id)
    elif current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Apply filters
    if status:
        query = query.filter(Appointment.status == status)
    if date_from:
        query = query.filter(Appointment.appointment_time >= date_from)
    if date_to:
        query = query.filter(Appointment.appointment_time <= date_to)

    # Add name-based searching
    if doctor_name:
        query = query.join(User, Appointment.doctor_id == User.id)\
                    .filter(User.full_name.ilike(f"%{doctor_name}%"))
    
    if patient_name:
        query = query.join(User, Appointment.patient_id == User.id)\
                    .filter(User.full_name.ilike(f"%{patient_name}%"))

    appointments = query.all()
    return appointments


# ----------------------------------------------------------
# Trigger monthly report generation (test only)
@router.get("/report/test")
def test_generate_monthly_report():
    generate_monthly_doctor_report.delay()
    return {"message": "Monthly report generation triggered"}

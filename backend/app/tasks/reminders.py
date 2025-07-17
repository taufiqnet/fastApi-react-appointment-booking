from app.celery_app import celery
from app.core.mail import send_email
from app.db.database import SessionLocal
from app.db.models.appointment import Appointment
from app.db.models.user import User
from datetime import datetime, timedelta

@celery.task
def send_appointment_reminders():
    db = SessionLocal()
    try:
        tomorrow = datetime.utcnow() + timedelta(days=1)
        appointments = db.query(Appointment).filter(
            Appointment.appointment_time.between(
                tomorrow.replace(hour=0, minute=0),
                tomorrow.replace(hour=23, minute=59)
            ),
            Appointment.status == "Confirmed"
        ).all()

        for appt in appointments:
            patient = db.query(User).filter(User.id == appt.patient_id).first()
            doctor = db.query(User).filter(User.id == appt.doctor_id).first()
            if patient:
                send_email(
                    to=patient.email,
                    subject="🔔 Appointment Reminder",
                    body=f"Reminder: Appointment with Dr. {doctor.full_name} at {appt.appointment_time}"
                )
    finally:
        db.close()

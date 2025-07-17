from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.appointment import Appointment
from app.db.models.user import User
from app.core.mail import send_email
from app.celery_app import celery

@celery.task
def generate_monthly_doctor_report():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = now

        # Get all doctors
        doctors = db.query(User).filter(User.user_type == "doctor").all()

        for doctor in doctors:
            appointments = db.query(Appointment).filter(
                Appointment.doctor_id == doctor.id,
                Appointment.appointment_time >= first_day,
                Appointment.appointment_time <= last_day,
                Appointment.status.in_(["Confirmed", "Completed"])
            ).all()

            total_visits = len(appointments)
            total_earned = sum(a.consultation_fee or 0 for a in appointments)
            patient_ids = set(a.patient_id for a in appointments)

            report_text = f"""
📅 Monthly Report for Dr. {doctor.full_name}
──────────────────────────────────────────────
🧍 Total Patients Seen: {len(patient_ids)}
📋 Total Appointments : {total_visits}
💰 Total Earnings     : BDT {total_earned:.2f}
──────────────────────────────────────────────
Generated on: {now.strftime('%Y-%m-%d')}
"""

            # Send report via email
            send_email(
                to=doctor.email,
                subject="📊 Your Monthly Appointment Report",
                body=report_text
            )

    finally:
        db.close()

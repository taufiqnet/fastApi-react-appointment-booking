from celery.schedules import crontab
from app.celery_app import celery

celery.conf.beat_schedule = {
    "send-reminders-every-morning": {
        "task": "app.tasks.reminders.send_appointment_reminders",
        "schedule": crontab(hour=7, minute=0),  # every day at 7AM UTC
    }
}


from celery.schedules import crontab
from app.celery_app import celery

celery.conf.beat_schedule.update({
    "monthly-doctor-report": {
        "task": "app.tasks.report.generate_monthly_doctor_report",
        "schedule": crontab(day_of_month=1, hour=2, minute=0),  # Runs 2 AM on 1st of every month
    }
})


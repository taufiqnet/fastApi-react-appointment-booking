import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to

    with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, to, msg.as_string())

# import os
# from dotenv import load_dotenv
# load_dotenv()

# class Settings:
#     JWT_SECRET = os.getenv("JWT_SECRET", "secretkey")
#     JWT_ALGORITHM = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
#     DB_URL = os.getenv("DATABASE_URL")

# settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Settings:
    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "secretkey")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))

    # Database
    DB_URL = os.getenv("DATABASE_URL")

    # Redis (for Celery)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Email (SMTP)
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

settings = Settings()

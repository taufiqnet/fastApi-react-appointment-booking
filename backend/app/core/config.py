import os
from dotenv import load_dotenv

# Load a .env.test file if it exists, otherwise load .env
dotenv_path = '.env.test' if os.path.exists('.env.test') else '.env'
load_dotenv(dotenv_path=dotenv_path)

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

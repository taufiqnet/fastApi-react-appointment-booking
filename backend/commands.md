

pip install fastapi uvicorn python-multipart python-dotenv sqlalchemy mysql-connector-python passlib[bcrypt] python-jose[cryptography] apscheduler pydantic email-validator

pip freeze > requirements.txt

python -m app.db.seed
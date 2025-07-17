from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.schemas.user import LoginSchema, TokenSchema
from app.db.crud.user import get_user_by_email
from app.core.security import verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.db.schemas.user import UserCreate, UserOut
from app.db.crud.user import create_user

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = create_user(db, data)
    return user


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token with user_type
    token = create_access_token(data={
        "sub": user.email,
        "user_id": user.id,
        "user_type": user.user_type.value if hasattr(user.user_type, "value") else user.user_type
    })

    # ✅ Return user_type explicitly in response
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": user.user_type.value if hasattr(user.user_type, "value") else user.user_type,
        "email": user.email
    }



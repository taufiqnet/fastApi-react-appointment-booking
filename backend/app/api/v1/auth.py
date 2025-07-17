from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.schemas.user import LoginSchema, TokenSchema, UserCreate, UserOut
from app.db.crud.user import get_user_by_email, create_user, get_user_by_mobile
from app.core.security import verify_password, create_access_token
import os
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads/profile_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/register", response_model=UserOut)
async def register(
    full_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(...),
    password: str = Form(...),
    user_type: str = Form(...),
    division: str = Form(None),
    district: str = Form(None),
    thana: str = Form(None),
    license_number: str = Form(None),
    experience_years: int = Form(None),
    consultation_fee: float = Form(None),
    available_timeslots: str = Form(None),
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_user = get_user_by_mobile(db, mobile_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    # Save the profile image to the filesystem
    file_extension = os.path.splitext(profile_image.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await profile_image.read())

    user_data = UserCreate(
        full_name=full_name,
        email=email,
        mobile_number=mobile_number,
        password=password,
        user_type=user_type,
        division=division,
        district=district,
        thana=thana,
        profile_image=file_path,
        license_number=license_number,
        experience_years=experience_years,
        consultation_fee=consultation_fee,
        available_timeslots=available_timeslots,
    )

    user = create_user(db, user_data, file_path)
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

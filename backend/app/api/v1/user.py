import logging
from app.db.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.database import SessionLocal
from app.core.security import get_current_user
from app.db.schemas.user import UserCreate, UserOut
from app.db.crud import user as user_crud

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/test")
def test_user():
    logger.info("✅ User test route called")
    return {"message": "✅ User route is working"}


from app.db.database import get_db


from typing import Optional
from app.utils.form_data import form_body

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate = Depends(form_body(UserCreate)), profile_image: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        if user_crud.get_user_by_email(db, user_data.email):
            logger.warning(f"❌ Registration failed: Email {user_data.email} already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check if mobile already exists
        if user_crud.get_user_by_mobile(db, user_data.mobile_number):
            logger.warning(f"❌ Registration failed: Mobile {user_data.mobile_number} already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number already registered"
            )

        image_data = await profile_image.read() if profile_image else None


        new_user = user_crud.create_user(db, user_data, image_data)
        logger.info(f"✅ New user registered: {user_data.email}")
        return new_user

    except IntegrityError as e:
        db.rollback()
        err_msg = str(e).lower()
        logger.error(f"⚠️ IntegrityError during registration: {err_msg}")
        if "mobile_number" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number already registered"
            )
        if "email" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed due to integrity error"
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.exception("❌ Unexpected error during registration")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )

@router.get("/users/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


from fastapi import Query

@router.get("/users/doctors")
def get_all_doctors(db: Session = Depends(get_db), name: str = Query(None)):
    print("Fetching doctors")
    query = db.query(User).filter(User.user_type == "doctor")
    if name:
        query = query.filter(User.full_name.ilike(f"%{name}%"))

    doctors = query.all()
    print(f"Found {len(doctors)} doctors")
    return [
        {
            "id": doc.id,
            "full_name": doc.full_name,
            "available_timeslots": doc.available_timeslots,
            "consultation_fee": doc.consultation_fee,
        }
        for doc in doctors
    ]

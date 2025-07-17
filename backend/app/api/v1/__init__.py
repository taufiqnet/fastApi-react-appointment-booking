from fastapi import APIRouter
from . import user, auth, appointment

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(appointment.router, prefix="/appointment", tags=["Appointment"])
router.include_router(appointment.router, prefix="/report", tags=["Report"])


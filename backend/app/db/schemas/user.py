<<<<<<< HEAD
import re
import logging
from typing import Optional, Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    constr,
    Field,
    validator,
    model_validator
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: constr(min_length=14, max_length=14)
    user_type: Literal["admin", "doctor", "patient"]
    division: Optional[str] = None
    district: Optional[str] = None
    thana: Optional[str] = None
    profile_image: Optional[bytes] = None

    license_number: Optional[str] = Field(default=None, validate_default=True)
    experience_years: Optional[int] = Field(default=None, validate_default=True)
    consultation_fee: Optional[float] = Field(default=None, validate_default=True)
    available_timeslots: Optional[str] = Field(default=None, validate_default=True)

    @validator('mobile_number')
    def mobile_number_must_be_valid(cls, v):
        pattern = r"^\+88\d{11}$"
        if not re.match(pattern, v):
            logger.warning(f"❌ Invalid mobile number: {v}")
            raise ValueError("mobile_number must match pattern +88 followed by 11 digits")
        return v

class UserCreate(UserBase):
    password: constr(min_length=8)

    @validator("password")
    def strong_password(cls, v):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])', v):
            logger.warning("❌ Weak password attempted during registration.")
            raise ValueError("Password must include 1 uppercase, 1 digit, 1 special char")
        return v

    @model_validator(mode='after')
    def validate_doctor_fields(self):
        if self.user_type == "doctor":
            missing = []
            if not self.license_number:
                missing.append("license_number")
            if self.experience_years is None:
                missing.append("experience_years")
            if self.consultation_fee is None:
                missing.append("consultation_fee")
            if not self.available_timeslots:
                missing.append("available_timeslots")
            if missing:
                logger.warning(f"❌ Doctor registration missing fields: {missing}")
                raise ValueError(f"The following fields are required for doctors: {', '.join(missing)}")
        return self

class UserOut(UserBase):
    id: int
    user_type: str
    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
=======
import re
import logging
from typing import Optional, Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    constr,
    Field,
    validator,
    model_validator
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: constr(min_length=14, max_length=14)
    user_type: Literal["admin", "doctor", "patient"]
    division: Optional[str] = None
    district: Optional[str] = None
    thana: Optional[str] = None
    profile_image: Optional[str] = None

    license_number: Optional[str] = Field(default=None, validate_default=True)
    experience_years: Optional[int] = Field(default=None, validate_default=True)
    consultation_fee: Optional[float] = Field(default=None, validate_default=True)
    available_timeslots: Optional[str] = Field(default=None, validate_default=True)

    @validator('mobile_number')
    def mobile_number_must_be_valid(cls, v):
        pattern = r"^\+88\d{11}$"
        if not re.match(pattern, v):
            logger.warning(f"❌ Invalid mobile number: {v}")
            raise ValueError("mobile_number must match pattern +88 followed by 11 digits")
        return v

class UserCreate(UserBase):
    password: constr(min_length=8)

    @validator("password")
    def strong_password(cls, v):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])', v):
            logger.warning("❌ Weak password attempted during registration.")
            raise ValueError("Password must include 1 uppercase, 1 digit, 1 special char")
        return v

    @model_validator(mode='after')
    def validate_doctor_fields(self):
        if self.user_type == "doctor":
            missing = []
            if not self.license_number:
                missing.append("license_number")
            if self.experience_years is None:
                missing.append("experience_years")
            if self.consultation_fee is None:
                missing.append("consultation_fee")
            if not self.available_timeslots:
                missing.append("available_timeslots")
            if missing:
                logger.warning(f"❌ Doctor registration missing fields: {missing}")
                raise ValueError(f"The following fields are required for doctors: {', '.join(missing)}")
        return self

class UserOut(UserBase):
    id: int
    user_type: str
    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
>>>>>>> 32db5770376e2b4a45d4de9155b1b355957b5b69

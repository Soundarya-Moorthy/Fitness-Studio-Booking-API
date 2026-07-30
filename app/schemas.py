
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

# ---------- User / Auth schemas ----------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = {"from_attributes": True}
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Fitness Class schemas ----------

class ClassCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    dateTime: datetime 
    instructor: str = Field(..., min_length=1, max_length=100)
    availableSlots: int = Field(..., ge=0)

    @field_validator("dateTime")
    @classmethod
    def must_have_tzinfo(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError(
                "dateTime must include timezone info, e.g. 2025-06-15T10:00:00+05:30"
            )
        return v

class ClassOut(BaseModel):
    id: int
    name: str
    dateTime: datetime 
    instructor: str
    availableSlots: int

    class Config:
        from_attributes = True

# ---------- Booking schemas ----------

class BookingCreate(BaseModel):
    class_id: int
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    class_name: str
    instructor: str
    dateTime: datetime
    client_name: str
    client_email: EmailStr
    booked_at: datetime

    class Config:
        from_attributes = True
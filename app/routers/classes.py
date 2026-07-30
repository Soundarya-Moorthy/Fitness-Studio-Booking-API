
from datetime import datetime, timezone
from typing import List
import pytz
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FitnessClass, User
from app.schemas import ClassCreate, ClassOut
from app.auth import get_current_user
from app.config import settings

router = APIRouter()

IST = pytz.timezone(settings.TIMEZONE)

def to_ist(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST)

def to_utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc)

@router.post("/classes", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    class_in: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    new_class = FitnessClass(
        name=class_in.name,
        date_time=to_utc(class_in.dateTime),
        instructor=class_in.instructor,
        available_slots=class_in.availableSlots,
        created_by=current_user.id,
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return ClassOut(
        id=new_class.id,
        name=new_class.name,
        dateTime=to_ist(new_class.date_time),
        instructor=new_class.instructor,
        availableSlots=new_class.available_slots,
    )


@router.get("/classes", response_model=List[ClassOut])
def list_upcoming_classes(db: Session = Depends(get_db)):
 
    now_utc = datetime.now(timezone.utc)
    classes = (
        db.query(FitnessClass)
        .filter(FitnessClass.date_time >= now_utc)
        .order_by(FitnessClass.date_time.asc())
        .all()
    )

    return [
        ClassOut(
            id=c.id,
            name=c.name,
            dateTime=to_ist(c.date_time),
            instructor=c.instructor,
            availableSlots=c.available_slots,
        )
        for c in classes
    ]
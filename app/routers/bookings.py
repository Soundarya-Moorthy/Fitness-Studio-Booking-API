
from datetime import timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking, FitnessClass, User
from app.schemas import BookingCreate, BookingOut
from app.auth import get_current_user
from app.routers.classes import to_ist

router = APIRouter()

@router.post("/book", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def book_class(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fitness_class = (
        db.query(FitnessClass)
        .filter(FitnessClass.id == booking_in.class_id)
        .first()
    )
    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found",
        )

    if fitness_class.available_slots <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available slots for this class",
        )

    fitness_class.available_slots -= 1
    new_booking = Booking(
        user_id=current_user.id,
        class_id=fitness_class.id,
        client_name=booking_in.client_name,
        client_email=booking_in.client_email,
    )
    db.add(new_booking)
    db.add(fitness_class)
    db.commit()
    db.refresh(new_booking)
    db.refresh(fitness_class)

    return BookingOut(
        id=new_booking.id,
        class_id=fitness_class.id,
        class_name=fitness_class.name,
        instructor=fitness_class.instructor,
        dateTime=to_ist(fitness_class.date_time),
        client_name=new_booking.client_name,
        client_email=new_booking.client_email,
        booked_at=new_booking.booked_at.replace(tzinfo=timezone.utc),
    )

@router.get("/bookings", response_model=List[BookingOut])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .all()
    )

    return [
        BookingOut(
            id=b.id,
            class_id=b.fitness_class.id,
            class_name=b.fitness_class.name,
            instructor=b.fitness_class.instructor,
            dateTime=to_ist(b.fitness_class.date_time),
            client_name=b.client_name,
            client_email=b.client_email,
            booked_at=b.booked_at.replace(tzinfo=timezone.utc),
        )
        for b in bookings
    ]
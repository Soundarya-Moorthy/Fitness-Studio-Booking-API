
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    classes_created = relationship("FitnessClass", back_populates="creator")
    bookings = relationship("Booking", back_populates="user")


class FitnessClass(Base):
    __tablename__ = "fitness_classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_time = Column(DateTime(timezone=True), nullable=False)  # stored in UTC
    instructor = Column(String, nullable=False)
    available_slots = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    creator = relationship("User", back_populates="classes_created")
    bookings = relationship("Booking", back_populates="fitness_class")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("fitness_classes.id"), nullable=False)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    booked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="bookings")
    fitness_class = relationship("FitnessClass", back_populates="bookings")
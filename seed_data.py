
from datetime import datetime, timedelta
import pytz

from app.database import SessionLocal, Base, engine
from app.models import FitnessClass
from app.config import settings

IST = pytz.timezone(settings.TIMEZONE)

def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_count = db.query(FitnessClass).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} class(es). Skipping seed.")
            print("Delete fitness.db and re-run this script if you want a fresh seed.")
            return

        now_ist = datetime.now(IST)

        sample_classes = [
            {
                "name": "Yoga Flow",
                "date_time": now_ist + timedelta(days=1, hours=2),
                "instructor": "John Doe",
                "available_slots": 20,
            },
            {
                "name": "Zumba Blast",
                "date_time": now_ist + timedelta(days=2, hours=4),
                "instructor": "Maria Lopez",
                "available_slots": 15,
            },
            {
                "name": "HIIT Session",
                "date_time": now_ist + timedelta(days=3, hours=1),
                "instructor": "Jane Smith",
                "available_slots": 10,
            },
            {
                "name": "Pilates Basics",
                "date_time": now_ist + timedelta(days=4, hours=3),
                "instructor": "Emily Carter",
                "available_slots": 12,
            },
            {
                "name": "Spin Cycle",
                "date_time": now_ist + timedelta(days=5, hours=5),
                "instructor": "Mike Chen",
                "available_slots": 18,
            },
        ]

        for class_data in sample_classes:
        
            utc_dt = class_data["date_time"].astimezone(pytz.utc)
            new_class = FitnessClass(
                name=class_data["name"],
                date_time=utc_dt,
                instructor=class_data["instructor"],
                available_slots=class_data["available_slots"],
                created_by=None,  # seeded data has no creator user
            )
            db.add(new_class)

        db.commit()
        print(f"Seeded {len(sample_classes)} fitness classes successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
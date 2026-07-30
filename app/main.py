
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth_routes, classes, bookings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Studio Booking API",
    description="A simple booking API for a fictional fitness studio "
                "(Yoga, Zumba, HIIT, etc.) with JWT authentication.",
    version="1.0.0",
)

app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(classes.router, tags=["Classes"])
app.include_router(bookings.router, tags=["Bookings"])

@app.get("/", tags=["Health"])
def root():
    """Simple health-check endpoint."""
    return {"status": "ok", "message": "Fitness Studio Booking API is running"}
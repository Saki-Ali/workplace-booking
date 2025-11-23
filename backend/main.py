from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud, seed_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workplace Booking MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_data.seed_workplaces(db)
    db.close()


@app.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest):
    return schemas.LoginResponse(token="dummy-token", user=payload.username)


@app.get("/workplaces", response_model=List[schemas.WorkplaceOut])
def list_workplaces(db: Session = Depends(get_db)):
    return crud.get_workplaces(db)


@app.get("/bookings", response_model=List[schemas.BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db)
    return [
        schemas.BookingOut(id=b.id, workplace_id=b.workplace_id, user=b.user)
        for b in bookings
    ]


@app.post("/bookings", response_model=schemas.BookingOut, status_code=201)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    booking = crud.create_booking(db, payload)
    return schemas.BookingOut(id=booking.id, workplace_id=booking.workplace_id, user=booking.user)


@app.delete("/bookings/{booking_id}", status_code=204)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    crud.delete_booking(db, booking_id)
    return None


@app.get("/")
def root():
    return {"message":"Ali's backend is running!"}

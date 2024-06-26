from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud
import models
import schemas
from models import Flight
from routers.v1.users import auth
from schemas import FlightCreate

from database import get_db

router = APIRouter()


@router.post('/bookings/', response_model=schemas.Booking)
async def create_booking(
        booking: schemas.BookingCreate, db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_booking(db=db, booking=booking, user_id=current_user.id)


@router.get('/bookings/', response_model=List[schemas.Booking])
async def read_user_bookings(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_user_bookings(db=db, user_id=current_user.id)


@router.post('/flights/', status_code=status.HTTP_201_CREATED)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


@router.get('/flights/')
def read_flights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    flights = db.query(Flight).offset(skip).limit(limit).all()
    return flights

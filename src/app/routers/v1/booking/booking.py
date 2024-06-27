from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from models import Flight
from routers.v1.users import auth
from schemas import FlightCreate

from database import get_db

router = APIRouter()

# @router.post('/bookings/', response_model=schemas.Booking)
# async def create_booking(
#         booking: schemas.BookingCreate,
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(auth.get_current_user)
# ):
#     db_booking = crud.create_booking(db=db, booking=booking, user_id=current_user.id)
#     if not db_booking:
#         raise HTTPException(status_code=400, detail="Unable to create booking")
#     return db_booking
#
# @router.get('/bookings/', response_model=List[schemas.Booking])
# async def read_user_bookings(
#         db: Session = Depends(get_db),
#         current_user: models.User = Depends(auth.get_current_user)
# ):
#     bookings = crud.get_user_bookings(db=db, user_id=current_user.id)
#     if bookings is None:
#         raise HTTPException(status_code=404, detail="Bookings not found")
#     return bookings

@router.post('/flights/', status_code=status.HTTP_201_CREATED, response_model=schemas.Flight)
async def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

@router.get('/flights/', response_model=List[schemas.Flight])
async def read_flights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    flights = db.query(Flight).offset(skip).limit(limit).all()
    return flights


@router.post('/bookings/', response_model=schemas.Booking)
async def create_booking(
        booking: schemas.BookingCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    # Получение данных о полете
    flight = db.query(models.Flight).filter(models.Flight.id == booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    # Создание бронирования
    db_booking = crud.create_booking(
        db=db,
        booking=schemas.BookingCreate(
            destination=flight.destination,
            price=flight.price,
            flight_id=flight.id
        ),
        user_id=current_user.id
    )
    return db_booking


@router.get('/bookings/', response_model=List[schemas.Booking])
async def read_user_bookings(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    bookings = crud.get_user_bookings(db=db, user_id=current_user.id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings
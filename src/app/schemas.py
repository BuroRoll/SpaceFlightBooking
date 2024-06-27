from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    bookings: List["Booking"] = []

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    destination: str
    price: str
    date: str


class BookingCreate(BookingBase):
    flight_id: int


class Booking(BookingBase):
    id: int
    date: str
    user_id: int
    flight_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class FlightBase(BaseModel):
    destination: str
    price: str
    date: str
    description: str
    planet_image: str


class FlightCreate(FlightBase):
    pass


class Flight(FlightBase):
    id: int

    class Config:
        from_attributes = True

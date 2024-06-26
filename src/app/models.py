from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    bookings = relationship("Booking", back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    destination = Column(String)
    price = Column(String)
    date = Column(String)
    user = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True)
    price = Column(String)
    date = Column(String)
    description = Column(String)
    planet_image = Column(String)
    bookings = relationship("Booking", back_populates="flight")

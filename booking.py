from fastapi import APIRouter, HTTPException
from typing import List
from models import Booking
from schemas import BookingRequest, BookingResponse
import datetime

router = APIRouter()

# Mock data
mock_bookings = []
booking_counter = 0

@router.post("/", response_model=BookingResponse)
async def create_booking(booking_request: BookingRequest):
    """Create a new booking"""
    global booking_counter
    booking_counter += 1
    
    # In a real app, you would validate bus exists and has seats
    booking = Booking(
        id=booking_counter,
        bus_id=booking_request.bus_id,
        passenger_name=booking_request.passenger_name,
        passenger_phone=booking_request.passenger_phone,
        passenger_count=booking_request.passenger_count,
        total_fare=booking_request.passenger_count * 150.0,  # Mock fare calculation
        booking_time=datetime.datetime.now().isoformat(),
        status="CONFIRMED"
    )
    
    mock_bookings.append(booking)
    
    return BookingResponse(
        booking_id=booking.id,
        bus_id=booking.bus_id,
        passenger_name=booking.passenger_name,
        passenger_count=booking.passenger_count,
        total_fare=booking.total_fare,
        booking_time=booking.booking_time,
        status=booking.status,
        message="Booking confirmed successfully!"
    )

@router.get("/{booking_id}")
async def get_booking(booking_id: int):
    """Get booking details"""
    for booking in mock_bookings:
        if booking.id == booking_id:
            return booking
    
    raise HTTPException(status_code=404, detail="Booking not found")
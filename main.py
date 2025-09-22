from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime, time
from schemas import *
from schemas import *
from schemas import Booking
from search import search_buses

app = FastAPI(
    title="Busify API",
    description="Unified Online Booking for Indian Government Buses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mock data for demonstration
mock_buses = [
    Bus(
        id=1,
        bus_number="UP 53 AB 1234",
        operator="UPSRTC",
        source="Meerut",
        destination="Delhi",
        departure_time="06:00",
        arrival_time="08:30",
        total_seats=50,
        available_seats=10,
        fare=150.0,
        bus_type="AC Seater",
        amenities=["Water Bottle", "Charging Point", "Blanket"],
        current_location="Near Roorkee"
    ),
    Bus(
        id=2,
        bus_number="DL 01 CD 5678",
        operator="DTC",
        source="Meerut",
        destination="Delhi",
        departure_time="07:30",
        arrival_time="10:00",
        total_seats=50,
        available_seats=2,
        fare=180.0,
        bus_type="Non-AC Seater",
        amenities=["Water Bottle"],
        current_location="Near Muzaffarnagar"
    ),
    Bus(
        id=3,
        bus_number="HR 22 EF 9012",
        operator="Haryana Roadways",
        source="Chandigarh",
        destination="Delhi",
        departure_time="08:00",
        arrival_time="11:30",
        total_seats=45,
        available_seats=25,
        fare=120.0,
        bus_type="AC Seater",
        amenities=["Water Bottle", "Charging Point", "Newspaper"],
        current_location="Near Ambala"
    ),
    Bus(
        id=4,
        bus_number="UP 32 GH 3456",
        operator="UPSRTC",
        source="Lucknow",
        destination="Kanpur",
        departure_time="09:00",
        arrival_time="12:00",
        total_seats=55,
        available_seats=8,
        fare=200.0,
        bus_type="AC Sleeper",
        amenities=["Water Bottle", "Charging Point", "Blanket", "Pillow"],
        current_location="Near Unnao"
    )
]

mock_bookings = []

@app.get("/")
async def root():
    return {
        "message": "Welcome to Busify API - Unified Online Booking for Indian Government Buses",
        "version": "1.0.0",
        "endpoints": {
            "search_buses_endpoint": "/api/buses/search",
            "get_bus": "/api/buses/{bus_id}",
            "book_ticket": "/api/bookings",
            "get_booking": "/api/bookings/{booking_id}"
        }
    }

@app.get("/api/buses", response_model=List[Bus])
async def get_all_buses():
    """Get all available buses"""
    return mock_buses

@app.get("/api/buses/search", response_model=List[BusResponse])
async def search_buses_endpoint(
    source: str,
    destination: str,
    date: Optional[str] = None
):
    """
    Search buses by source and destination
    """
    buses = search_buses(mock_buses, source, destination, date)
    return buses

@app.get("/api/buses/{bus_id}", response_model=BusDetail)
async def get_bus_details(bus_id: int):
    """Get detailed information for a specific bus"""
    for bus in mock_buses:
        if bus.id == bus_id:
            availability_score = calculate_availability_score(
                bus.total_seats, bus.available_seats
            )
            return BusDetail(
                id=bus.id,
                bus_number=bus.bus_number,
                operator=bus.operator,
                source=bus.source,
                destination=bus.destination,
                departure_time=bus.departure_time,
                arrival_time=bus.arrival_time,
                total_seats=bus.total_seats,
                available_seats=bus.available_seats,
                fare=bus.fare,
                bus_type=bus.bus_type,
                amenities=bus.amenities,
                availability_score=availability_score,
                current_location=bus.current_location
            )
    
    raise HTTPException(status_code=404, detail="Bus not found")

@app.post("/api/bookings", response_model=BookingResponse)
async def create_booking(booking_request: BookingRequest):
    """Create a new booking"""
    # Find the bus
    bus = None
    for b in mock_buses:
        if b.id == booking_request.bus_id:
            bus = b
            break
    
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    # Check seat availability
    if bus.available_seats < booking_request.passenger_count:
        raise HTTPException(status_code=400, detail="Not enough seats available")
    
    # Create booking
    booking_id = len(mock_bookings) + 1
    booking = Booking(
        id=booking_id,
        bus_id=booking_request.bus_id,
        passenger_name=booking_request.passenger_name,
        passenger_phone=booking_request.passenger_phone,
        passenger_email=booking_request.passenger_email,
        passenger_count=booking_request.passenger_count,
        total_fare=bus.fare * booking_request.passenger_count,
        booking_time=datetime.now().isoformat(),
        status="CONFIRMED"
    )
    
    mock_bookings.append(booking)
    
    # Update bus availability (in real app, this would be in database)
    for b in mock_buses:
        if b.id == booking_request.bus_id:
            b.available_seats -= booking_request.passenger_count
            break
    
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

@app.get("/api/bookings/{booking_id}", response_model=Booking)
async def get_booking(booking_id: int):
    """Get booking details by ID"""
    for booking in mock_bookings:
        if booking.id == booking_id:
            return booking
    
    raise HTTPException(status_code=404, detail="Booking not found")

@app.get("/api/buses/{bus_id}/location")
async def get_bus_location(bus_id: int):
    """Get current location of a specific bus"""
    for bus in mock_buses:
        if bus.id == bus_id:
            return {"bus_id": bus.id, "current_location": bus.current_location}

    raise HTTPException(status_code=404, detail="Bus not found")

def calculate_availability_score(total_seats: int, available_seats: int) -> int:
    """
    Calculate availability score (1-100)
    Higher score = better chance of getting seat
    """
    if total_seats == 0:
        return 0
    
    percentage = (available_seats / total_seats) * 100
    
    # Convert percentage to score (1-100)
    if percentage >= 50:
        return 100  # High availability
    elif percentage >= 20:
        return 50   # Medium availability
    elif percentage > 0:
        return int(percentage)  # Low availability
    else:
        return 0    # No seats available

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5100)
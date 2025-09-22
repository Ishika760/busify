from fastapi import APIRouter, HTTPException
from typing import List
from schemas import Bus
from schemas import BusResponse

router = APIRouter()

# Mock data
mock_buses = [
    Bus(1, "UP 53 AB 1234", "UPSRTC", "Meerut", "Delhi", "06:00", "08:30", 50, 10, 150.0),
    Bus(2, "DL 01 CD 5678", "DTC", "Meerut", "Delhi", "07:30", "10:00", 50, 2, 180.0),
    Bus(3, "HR 22 EF 9012", "Haryana Roadways", "Chandigarh", "Delhi", "08:00", "11:30", 45, 25, 120.0)
]

@router.get("/", response_model=List[BusResponse])
async def get_all_buses():
    """Get all available buses"""
    response = []
    for bus in mock_buses:
        availability_score = main.calculate_availability_score(bus.total_seats, bus.available_seats)
        response.append(BusResponse(
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
            availability_score=availability_score
        ))
    return response

@router.get("/{bus_id}", response_model=BusResponse)
async def get_bus(bus_id: int):
    """Get specific bus details"""
    for bus in mock_buses:
        if bus.id == bus_id:
            availability_score = calculate_availability_score(bus.total_seats, bus.available_seats)
            return BusResponse(
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
                availability_score=availability_score
            )
    
    raise HTTPException(status_code=404, detail="Bus not found")
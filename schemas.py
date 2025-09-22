from pydantic import BaseModel

class Bus(BaseModel):
    id: int
    bus_number: str
    operator: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    total_seats: int
    available_seats: int
    fare: float
    bus_type: str
    amenities: list[str]
    current_location: str
from typing import List, Optional, ClassVar
from pydantic import BaseModel

class Booking(BaseModel):
    id: int
    bus_id: int
    passenger_name: str
    passenger_phone: str
    passenger_count: int
    total_fare: float
    booking_time: str
    status: str

# Request Schemas
class SearchRequest(BaseModel):
    source: str
    destination: str
    date: Optional[str] = None

class BookingRequest(BaseModel):
    bus_id: int
    passenger_name: str
    passenger_phone: str
    passenger_email: Optional[str] = None
    passenger_count: int

# Response Schemas
class BusResponse(BaseModel):
    id: int
    bus_number: str
    operator: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    total_seats: int
    available_seats: int
    fare: float
    availability_score: int

class BookingResponse(BaseModel):
    booking_id: int
    bus_id: int
    passenger_name: str
    passenger_count: int
    total_fare: float
    booking_time: str
    status: str
    message: str

class ErrorResponse(BaseModel):
    detail: str

class BusDetail(BaseModel):
    id: int
    bus_number: str
    operator: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    total_seats: int
    available_seats: int
    fare: float
    bus_type: str
    amenities: list[str]
    availability_score: int
    current_location: str
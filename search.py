from fastapi import APIRouter
from typing import List
from schemas import Bus
from schemas import BusResponse

router = APIRouter()

def search_buses(
    buses: List[Bus],
    source: str,
    destination: str,
    date: str = None
) -> List[BusResponse]:
    """
    Search buses by source and destination
    """
    filtered_buses = []
    for bus in buses:
        if (bus.source.lower() == source.lower() and
            bus.destination.lower() == destination.lower()):
            # Calculate availability score
            availability_score = main.calculate_availability_score(
                bus.total_seats, bus.available_seats
            )

            bus_response = BusResponse(
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
            filtered_buses.append(bus_response)

    # Sort by departure time
    filtered_buses.sort(key=lambda x: x.departure_time)
    return filtered_buses
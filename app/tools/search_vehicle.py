from langchain_core.tools import tool

from app.services.vehicle_service import VehicleService
from app.models.SearchRequest import SearchRequest
from app.models.vehicle import Vehicle

vehicle_service = VehicleService(
    "data/vehicles.json"
)


@tool
def search_vehicles(request: SearchRequest) -> list[Vehicle]:
    """Search vehicles using the provided search criteria."""

    return vehicle_service.search(
        brand=request.brand,
        max_price=request.max_price,
        vehicle_type=request.vehicle_type,
    )

@tool
def get_vehicle_details(
    vehicle_id: int,
):
    """Get detailed information about a vehicle using its ID."""

    vehicle = vehicle_service.get_by_id(vehicle_id)

    if vehicle is None:
        return "Vehicle not found."

    return vehicle
from langchain_core.tools import tool

from app.services.vehicle_service import VehicleService


vehicle_service = VehicleService(
    "data/vehicles.json"
)


@tool
def search_vehicles(
    brand: str | None = None,
    max_price: int | None = None,
    vehicle_type: str | None = None,
):
    """Search vehicles by brand, maximum price, and vehicle type."""

    return vehicle_service.search(
        brand=brand,
        max_price=max_price,
        vehicle_type=vehicle_type,
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
import json

from app.models.vehicle import Vehicle


class VehicleService:

    def __init__(self, data_path: str):
        self._data_path = data_path
        self._vehicles = self._load_vehicles()

    def _load_vehicles(self) -> list[Vehicle]:
        with open(self._data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            Vehicle(**vehicle)
            for vehicle in data
        ]

    def search(
        self,
        brand: str | None = None,
        max_price: int | None = None,
        vehicle_type: str | None = None,
    ) -> list[Vehicle]:

        results = self._vehicles

        if brand:
            results = [
                vehicle
                for vehicle in results
                if vehicle.brand.lower() == brand.lower()
            ]

        if max_price is not None:
            results = [
                vehicle
                for vehicle in results
                if vehicle.price <= max_price
            ]

        if vehicle_type:
            results = [
                vehicle
                for vehicle in results
                if vehicle.vehicle_type.lower()
                == vehicle_type.lower()
            ]

        return results
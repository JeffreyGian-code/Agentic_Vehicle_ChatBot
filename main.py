from app.services.vehicle_service import VehicleService


service = VehicleService(
    "data/vehicles.json"
)

results = service.search(
    brand="Honda",
    max_price=1000000,
)

for vehicle in results:
    print(vehicle)
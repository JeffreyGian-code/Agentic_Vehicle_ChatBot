from app.services.vehicle_service import VehicleService


def create_service():
    return VehicleService(
        "data/vehicles.json"
    )


def test_search_by_brand_and_price():
    service = create_service()

    results = service.search(
        brand="Honda",
        max_price=1000000,
    )

    assert len(results) == 2

    names = [vehicle.name for vehicle in results]

    assert "Honda Amaze" in names
    assert "Honda City" in names



def test_get_vehicle_by_id():
    service = create_service()

    vehicle = service.get_by_id(1)

    assert vehicle is not None
    assert vehicle.name == "Honda Amaze"
    assert vehicle.brand == "Honda"

#missing vehicle test
def test_get_missing_vehicle():
    service = create_service()

    vehicle = service.get_by_id(999)

    assert vehicle is None
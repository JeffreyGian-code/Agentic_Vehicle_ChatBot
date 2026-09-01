import os

import pytest
from dotenv import load_dotenv

pytest.importorskip("psycopg")

from app.services.vehicle_service import VehicleService


load_dotenv()


def create_service():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        pytest.skip("DATABASE_URL is required for PostgreSQL integration tests.")

    return VehicleService(database_url)


def test_search_by_brand_and_price():
    service = create_service()

    results = service.search(
        brand="Honda",
        max_price=1000000,
    )

    assert len(results) == 5

    names = [vehicle.name for vehicle in results]

    assert "Amaze Base" in names
    assert "Amaze VX" in names



def test_get_vehicle_by_id():
    service = create_service()

    vehicle = service.get_by_id(1)

    assert vehicle is not None
    assert vehicle.name == "Amaze Base"
    assert vehicle.brand == "Honda"

#missing vehicle test
def test_get_missing_vehicle():
    service = create_service()

    vehicle = service.get_by_id(999)

    assert vehicle is None

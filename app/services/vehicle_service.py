from sqlalchemy import text

from app.database import engine
from app.models.vehicle import Vehicle


class VehicleService:
    """Reads vehicle data from PostgreSQL."""

    def search(
        self,
        brand: str | None = None,
        max_price: int | None = None,
        vehicle_type: str | None = None,
    ) -> list[Vehicle]:

        query = """
            SELECT id, name, brand, price, vehicle_type
            FROM vehicles
        """

        conditions: list[str] = []
        parameters: dict[str, str | int] = {}

        if brand:
            conditions.append("LOWER(brand) = LOWER(:brand)")
            parameters["brand"] = brand

        if max_price is not None:
            conditions.append("price <= :max_price")
            parameters["max_price"] = max_price

        if vehicle_type:
            conditions.append(
                "LOWER(vehicle_type) = LOWER(:vehicle_type)"
            )
            parameters["vehicle_type"] = vehicle_type

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY id"

        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                parameters,
            )

            rows = result.mappings().all()

        return [
            Vehicle.model_validate(row)
            for row in rows
        ]

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:

        query = """
            SELECT id, name, brand, price, vehicle_type
            FROM vehicles
            WHERE id = :vehicle_id
        """

        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                {"vehicle_id": vehicle_id},
            )

            row = result.mappings().first()

        return (
            Vehicle.model_validate(row)
            if row
            else None
        )
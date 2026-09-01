from app.database import get_connection
from app.models.vehicle import Vehicle


class VehicleService:
    """Reads vehicle data from PostgreSQL."""

    def __init__(self, database_url: str | None = None):
        self._database_url = database_url

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
        parameters: list[str | int] = []

        if brand:
            conditions.append("LOWER(brand) = LOWER(%s)")
            parameters.append(brand)

        if max_price is not None:
            conditions.append("price <= %s")
            parameters.append(max_price)

        if vehicle_type:
            conditions.append("LOWER(vehicle_type) = LOWER(%s)")
            parameters.append(vehicle_type)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY id"

        with get_connection(self._database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
                rows = cursor.fetchall()

        return [Vehicle.model_validate(row) for row in rows]

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        query = """
            SELECT id, name, brand, price, vehicle_type
            FROM vehicles
            WHERE id = %s
        """

        with get_connection(self._database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (vehicle_id,))
                row = cursor.fetchone()

        return Vehicle.model_validate(row) if row else None

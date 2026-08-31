from pydantic import BaseModel


class SearchRequest(BaseModel):
    brand: str | None = None
    max_price: int | None = None
    vehicle_type: str | None = None
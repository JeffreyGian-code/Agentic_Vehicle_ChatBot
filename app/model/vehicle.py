from pydantic import BaseModel

class Vehicle(BaseModel):
    id: int
    brand: str
    model: str
    price: int
    vehicle_type: str
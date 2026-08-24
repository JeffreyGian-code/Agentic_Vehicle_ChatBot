from pydantic import BaseModel

class Vehicle(BaseModel):
    id: int
    name: str
    brand: str
    price: int
    vehicle_type: str
from pydantic import BaseModel

class AddressRequest(BaseModel):
    pickup_address: str
    delivery_address: str
    delivery_category: str
    vehicle_type: str

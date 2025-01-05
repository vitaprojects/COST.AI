from fastapi import APIRouter, HTTPException
from models import AddressRequest
from utils import calculate_cost

calculate_router = APIRouter()

@calculate_router.post("/calculate-cost/")
async def calculate_cost_route(address: AddressRequest):
    """
    Route to calculate delivery cost.
    """
    result = calculate_cost(
        pickup_address=address.pickup_address,
        delivery_address=address.delivery_address,
        vehicle_type=address.vehicle_type,
        delivery_category=address.delivery_category,
    )
    return {
        "pickup_address": address.pickup_address,
        "delivery_address": address.delivery_address,
        **result
    }
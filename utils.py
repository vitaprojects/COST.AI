import os
import json
import logging
import requests
import traceback
import google.generativeai as genai
from fastapi import HTTPException
#from config import VEHICLE_TYPES, DELIVERY_CATEGORIES, GOOGLE_API_KEY, CurrentPetrolCostCanada
from config import VEHICLE_TYPES, DELIVERY_CATEGORIES, GOOGLE_API_KEY, ConstCurrentPetrolCostCanada

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Check .env file.")

genai.configure(api_key=GEMINI_API_KEY)

# Create the Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def get_category_details_from_gemini(delivery_category):
    """
    Use Gemini to get details for an unknown delivery category
    """
    try:
        logger.info(f"Attempting to get Gemini AI details for category: {delivery_category}")
        
        # Extended prompt with more context
        prompt = [
            "You are an intelligent assistant for logistics and delivery applications. Your role is to determine the appropriate delivery category modifier based on the provided delivery category. "
            "For an unknown delivery category, provide a reasonable cost modifier and recommended vehicle.Analyze the category name to assign a modifier in the range 0.7 to 1.3",
            "input: SENIOR APPOINTMENT", 
            "output: {\n \"modifier\": 0.7,\n \"rationale\": \"Senior appointments typically involve non-commercial transport and warrant a reduced cost.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: FLOWER DELIVERY", 
            "output: {\n \"modifier\": 1.2,\n \"rationale\": \"Flowers are perishable and delicate, requiring careful handling and timely delivery.\",\n \"recommended_vehicle\": \"Van\"\n}",
            "input: FURNITURE DELIVERY", 
            "output: {\n \"modifier\": 1.8,\n \"rationale\": \"Bulk furniture is heavy and requires a large vehicle with significant loading capacity.\",\n \"recommended_vehicle\": \"Flatbed Truck\"\n}",
            "input: CAKE DELIVERY", 
            "output: {\n \"modifier\": 1.3,\n \"rationale\": \"Cakes are fragile and often require temperature control to prevent spoilage.\",\n \"recommended_vehicle\": \"Reefers (Refrigerated Truck)\"\n}",
            "input: MEDICINE", 
            "output: {\n \"modifier\": 0.6,\n \"rationale\": \"Medical deliveries require precision and timely transport, often with special handling.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: GROCERY DELIVERY", 
            "output: {\n \"modifier\": 0.9,\n \"rationale\": \"Groceries need careful handling and moderate transportation requirements.\",\n \"recommended_vehicle\": \"Van\"\n}",
            "input: FOOD DELIVERY", 
            "output: {\n \"modifier\": 1.0,\n \"rationale\": \"Standard food delivery with typical transportation needs.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: CAR PARTS", 
            "output: {\n \"modifier\": 1.2,\n \"rationale\": \"Car parts vary in size and may require careful handling and protection.\",\n \"recommended_vehicle\": \"Pickup Truck\"\n}",
            "input: TORONTO LAB", 
            "output: {\n \"modifier\": 1.3,\n \"rationale\": \"Laboratory deliveries often require specialized handling and timely transport.\",\n \"recommended_vehicle\": \"Van\"\n}",
            "input: SENIOR (PACKAGE PICKUP)", 
            "output: {\n \"modifier\": 0.8,\n \"rationale\": \"Senior package pickups typically involve shorter, more considerate routes.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: SENIOR APPOINTMENT", 
            "output: {\n \"modifier\": 1.1,\n \"rationale\": \"Senior appointments require careful, comfortable transportation.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: CANNABIS DELIVERY", 
            "output: {\n \"modifier\": 1.2,\n \"rationale\": \"Regulated product requiring secure and discreet transportation.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: PICKUP TRUCK", 
            "output: {\n \"modifier\": 1.0,\n \"rationale\": \"Standard delivery with moderate transportation requirements.\",\n \"recommended_vehicle\": \"Pickup Truck\"\n}",
            "input: VAN DELIVERY", 
            "output: {\n \"modifier\": 1.0,\n \"rationale\": \"Standard van delivery with typical transportation needs.\",\n \"recommended_vehicle\": \"Van\"\n}",
            "input: STANDARD DELIVERY", 
            "output: {\n \"modifier\": 1.0,\n \"rationale\": \"Typical delivery with no special handling requirements.\",\n \"recommended_vehicle\": \"Car\"\n}",
            "input: FLOWER DELIVERY", 
            "output: {\n \"modifier\": 1.1,\n \"rationale\": \"Flowers require gentle handling and timely delivery.\",\n \"recommended_vehicle\": \"Van\"\n}",
            "input: CAR", 
            "output: {\n \"modifier\": 1.0,\n \"rationale\": \"Standard car transportation with no special requirements.\",\n \"recommended_vehicle\": \"Car\"\n}",
            f"input: {delivery_category}", 
            "output: "
        ]
        
        response = gemini_model.generate_content(prompt)
        
        # Log the raw response
        logger.info(f"Raw Gemini response: {response.text}")
        
        # Clean and parse the response
        gemini_output = response.text.strip().replace('```json', '').replace('```', '').strip()
        
        # Try parsing JSON
        try:
            parsed_output = json.loads(gemini_output)
            
            # Validate the parsed output
            if not (0.5 <= parsed_output.get('modifier', 1.0) <= 2.0):
                logger.warning(f"Invalid modifier: {parsed_output.get('modifier')}")
                return {'modifier': 1.0, 'vehicle_type': 'Car'}
            
            vehicle_type = parsed_output.get('recommended_vehicle', 'Car')
            
            # Validate vehicle type
            if vehicle_type not in VEHICLE_TYPES:
                logger.warning(f"Invalid vehicle type: {vehicle_type}")
                vehicle_type = 'Car'
            
            return {
                'modifier': parsed_output.get('modifier', 1.0),
                'vehicle_type': vehicle_type
            }
        
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from Gemini response: {gemini_output}")
            return {'modifier': 1.0, 'vehicle_type': 'Car'}
    
    except Exception as e:
        # Comprehensive error logging
        logger.error(f"Gemini AI error for category {delivery_category}:")
        logger.error(traceback.format_exc())
        return {
            'modifier': 1.0,
            'vehicle_type': 'Car'
        }
def generate_tiers_half_km():
    """
    Generate tiers with progressively increasing rates of decrement for every 0.5 km.
    Beyond 60 km, apply a constant decrease percentage.
    """
    tiers = []
    cumulative_decrease = 0.00  # Start with 0% decrease
    increment = 0.005  # Initial increment for the growth rate
    max_decrease = 0.95  # Cap the decrease at 95%
    max_distance = 60.0  # Maximum distance for progressive tiers in km
    constant_decrease = 0.96  # Constant decrease beyond 60 km

    for i in range(int(max_distance * 2)):  # Up to 60 km (120 x 0.5 km = 60 km)
        if i == 0:
            decrease = 0.00
        else:
            cumulative_decrease += increment
            increment += 0.005

            if cumulative_decrease > max_decrease:
                cumulative_decrease = max_decrease

        tiers.append((0.5, cumulative_decrease))

    # Add a final tier to indicate a flat rate decrease beyond 60 km
    tiers.append((float('inf'), constant_decrease))  # Infinite distance for the constant tier
    return tiers


def calculate_cost(pickup_address, delivery_address, vehicle_type, delivery_category):
    """
    Calculate delivery cost dynamically for each 0.5 km interval.
    """
    # Check if delivery category exists
    if delivery_category not in DELIVERY_CATEGORIES:
        logger.info(f"Unknown delivery category: {delivery_category}. Consulting Gemini AI.")
        gemini_category_details = get_category_details_from_gemini(delivery_category)
        category_modifier = gemini_category_details['modifier']
    else:
        category_modifier = DELIVERY_CATEGORIES[delivery_category]

    # Validate vehicle type
    if vehicle_type not in VEHICLE_TYPES:
        logger.warning(f"Invalid vehicle type: {vehicle_type}. Defaulting to Car.")
        vehicle_type = 'Car'

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": pickup_address,
        "destinations": delivery_address,
        "key": GOOGLE_API_KEY,
    }

    try:
        logger.info(f"Fetching distance between {pickup_address} and {delivery_address}")
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            logger.error(f"Google Maps API error: {data}")
            raise HTTPException(status_code=400, detail="Error fetching distance data")

        distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
        distance_value = data["rows"][0]["elements"][0]["distance"]["value"]  # in meters
        distance_km = distance_value / 1000  # Convert meters to kilometers

        logger.info(f"Distance calculated: {distance_km} km")

        vehicle = VEHICLE_TYPES[vehicle_type]
        base_rate = vehicle["base_rate"]
        fuel_efficiency = vehicle["fuel_efficiency"]
        fuel_cost_per_km = ConstCurrentPetrolCostCanada / fuel_efficiency
        cost_per_km = (base_rate + fuel_cost_per_km) * category_modifier

        tiers = generate_tiers_half_km()

        remaining_distance = distance_km
        total_cost = 0.0

        for tier_distance, decrease_percentage in tiers:
            if remaining_distance <= 0:
                break

            # Handle infinite tier for distances beyond 60 km
            if tier_distance == float('inf'):
                segment_distance = remaining_distance
            else:
                segment_distance = min(tier_distance, remaining_distance)

            adjusted_cost_per_km = cost_per_km * (1 - decrease_percentage)
            segment_cost = segment_distance * adjusted_cost_per_km

            total_cost += segment_cost
            remaining_distance -= segment_distance
            avg_cost_per_km = total_cost / distance_km
            if(avg_cost_per_km<.6):
                avg_cost_per_km=0.6
            final_cost=distance_km*avg_cost_per_km
            if(distance_km<4 and distance_km>0):
                if(round(distance_km,0)==1):
                    final_cost+=6
                elif(round(distance_km,0)==2):
                    final_cost+=4.8
                elif(round(distance_km,0)==3):
                    final_cost+=3.6
                elif(round(distance_km,0)==4):
                    final_cost+=2.4
            if(final_cost<5.7):
                final_cost=5.7

            logger.info(f"Segment: {segment_distance} km, Adjusted Cost/KM: ${adjusted_cost_per_km:.4f}, "
                        f"Segment Cost: ${segment_cost:.4f}")

        logger.info(f"Total Delivery Cost: ${total_cost}")

        return {
            "distance": distance_text,
            "total_cost": round(final_cost, 8),
            "average_cost_per_km": round(avg_cost_per_km, 8),
            "delivery_category_modifier": category_modifier,
        }
    except Exception as e:
        logger.error(f"Cost calculation error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

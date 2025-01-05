import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# File to store the petrol cost
PETROL_COST_FILE = "petrol_cost.json"

# Google API key
#GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_API_KEY = "AIzaSyBNImj-t02PTgHdecLieLJWCooT3eC0qs8"
if not GOOGLE_API_KEY:
    raise ValueError("Google Maps API key is missing. Check .env file.")

# Configure Gemini AI
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = "AIzaSyCR0d6QqpPKKDh4G-FTXcm_kxML5GqhbtY"
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Check .env file.")

genai.configure(api_key=GEMINI_API_KEY)

# Create the model
generation_config = {
    "temperature": 0,  # Makes the response deterministic
    "top_p": 1,        # Disable nucleus sampling (1 means no cutoff)
    "top_k": 1,        # Choose the single most probable token
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def fetch_petrol_cost():
    """Fetch current petrol cost using Gemini API."""
    print("Fetching current petrol cost from Gemini API...")
    response = model.generate_content([
    "You are an intelligent assistant for logistics and delivery applications. Your role is to determine the current price per liter of petrol in CAD for Canada. Provide the current price per liter of petrol/gasoline in CAD.Follow the input output for the response format but provide the actual currrent rate.",
    "input: current price per liter in CAD",
    "output: {\n    \"current_price_per_liter\": \"1.65\",\n    \"date\": \"2024-11-17\"\n}",
    "input: ",
    "output: ",
    ])

    try:
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        price_data = json.loads(cleaned_text)
        price_str = price_data.get("current_price_per_liter", "1.7")
        petrol_cost = float(price_str)
        return {"current_price_per_liter": petrol_cost, "date": datetime.now().strftime("%Y-%m-%d")}
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"Error fetching price: {e}")
        return {"current_price_per_liter": 1.7, "date": datetime.now().strftime("%Y-%m-%d")}  # Fallback value

def get_petrol_cost():
    """Get petrol cost from file or fetch new cost if outdated."""
    if os.path.exists(PETROL_COST_FILE):
        with open(PETROL_COST_FILE, "r") as file:
            data = json.load(file)
            if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                print("Loaded petrol cost from file.")
                print(f"DEBUG: Current Petrol Cost per Liter: ${data['current_price_per_liter']}")
                return data["current_price_per_liter"]

    # If the file is missing or outdated, fetch new data
    petrol_data = fetch_petrol_cost()
    with open(PETROL_COST_FILE, "w") as file:
        json.dump(petrol_data, file, indent=2)
    print("Updated petrol cost and saved to file.")
    return petrol_data["current_price_per_liter"]

# Get today's petrol cost
ConstCurrentPetrolCostCanada = get_petrol_cost()
#ConstCurrentPetrolCostCanada=1.5
# Vehicle types with dynamically calculated base rates
VEHICLE_TYPES = {
    "Car": {"base_rate": 0.95 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 14},
    "Van": {"base_rate": 1.5 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 10},
    "Pickup Truck": {"base_rate": 2.5 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 8},
    "Tow Truck": {"base_rate": 3.86 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 6},
    "Reefers (Refrigerated Truck)": {"base_rate": 4.97 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 5},
    "Box Truck": {"base_rate": 6.05 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 7},
    "Flatbed Truck": {"base_rate": 5.73 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 6},
}

# Delivery categories
DELIVERY_CATEGORIES = {
    "MEDICINE": 0.6,
    "GROCERY DELIVERY": 0.9,
    "FOOD DELIVERY": 1.0,
    "CAR PARTS": 1.2,
    "TORONTO LAB": 1.3,
    "SENIOR (PACKAGE PICKUP)": 0.8,
    "SENIOR APPOINTMENT": 1.1,
    "CANNABIS DELIVERY": 1.2,
    "PICKUP TRUCK": 1.0,
    "VAN DELIVERY": 1.0,
    "STANDARD DELIVERY": 1.0,
    "FLOWER DELIVERY": 1.1,
    "CAR": 1.0,
}

# Print the current petrol cost for verification
print(f"FINAL: Current Petrol Cost per Liter: ${ConstCurrentPetrolCostCanada}")

# Example of how base rates are now dynamically calculated
for vehicle, details in VEHICLE_TYPES.items():
    print(f"{vehicle} Base Rate: ${details['base_rate']:.2f}")



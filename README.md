```sh
python3 -m venv venv
. venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file with the following content:
```
GOOGLE_MAPS_API_KEY=<your_api_key>
GEMINI_API_KEY=<your_api_key>
```

### Running the Application
```sh
uvicorn main:app --reload
```
"""
All the initial configuration for calculating costing is in the config.py file.Do changes if needed
VEHICLE_TYPES: dict
  A dictionary containing different types of vehicles and their respective base rates and fuel efficiencies.
  The base rate is calculated as a multiple of the current petrol cost in Canada (CurrentPetrolCostCanada).
  The fuel efficiency is measured in kilometers per liter (km/l).

  Keys:
    "Car": dict
      - base_rate: float
        The base rate for a car.
      - fuel_efficiency: int
        The fuel efficiency of a car in km/l.
    "Van": dict
      - base_rate: float
        The base rate for a van.
      - fuel_efficiency: int
        The fuel efficiency of a van in km/l.
    "Pickup Truck": dict
      - base_rate: float
        The base rate for a pickup truck.
      - fuel_efficiency: int
        The fuel efficiency of a pickup truck in km/l.
    "Tow Truck": dict
      - base_rate: float
        The base rate for a tow truck.
      - fuel_efficiency: int
        The fuel efficiency of a tow truck in km/l.
    "Reefers (Refrigerated Truck)": dict
      - base_rate: float
        The base rate for a refrigerated truck.
      - fuel_efficiency: int
        The fuel efficiency of a refrigerated truck in km/l.
    "Box Truck": dict
      - base_rate: float
        The base rate for a box truck.
      - fuel_efficiency: int
        The fuel efficiency of a box truck in km/l.
    "Flatbed Truck": dict
      - base_rate: float
        The base rate for a flatbed truck.
      - fuel_efficiency: int
        The fuel efficiency of a flatbed truck in km/l.

DELIVERY_CATEGORIES: dict
  A dictionary containing different delivery categories and their respective multipliers.
  The multipliers are used to adjust the base rate for different types of deliveries.

  Keys:
    "MEDICINE": float
      Multiplier for medicine deliveries.
    "GROCERY DELIVERY": float
      Multiplier for grocery deliveries.
    "FOOD DELIVERY": float
      Multiplier for food deliveries.
    "CAR PARTS": float
      Multiplier for car parts deliveries.
    "TORONTO LAB": float
      Multiplier for Toronto lab deliveries.
    "SENIOR (PACKAGE PICKUP)": float
      Multiplier for senior package pickups.
    "SENIOR APPOINTMENT": float
      Multiplier for senior appointments.
    "CANNABIS DELIVERY": float
      Multiplier for cannabis deliveries.
    "PICKUP TRUCK": float
      Multiplier for pickup truck deliveries.
    "VAN DELIVERY": float
      Multiplier for van deliveries.
    "STANDARD DELIVERY": float
      Multiplier for standard deliveries.
    "FLOWER DELIVERY": float
      Multiplier for flower deliveries.
    "CAR": float
      Multiplier for car deliveries.
"""
### Test Data
```json
[
  {
    "pickup_address": "Toronto, ON",
    "delivery_address": "Mississauga, ON",
    "delivery_category": "MEDICINE",
    "vehicle_type": "Car"
  },
  {
    "pickup_address": "Churchville, brampton on",
    "delivery_address": "Coleraine Ontario L4H 2G4",
    "delivery_category": "CAR",
    "vehicle_type": "Car"
},
    {
    "pickup_address": "Churchville, brampton on",
    "delivery_address": "150 Central Park Dr, Brampton, ON L6T 2T9",
    "delivery_category": "CAR",
    "vehicle_type": "Car"
  },
{
    "pickup_address": "20 wexford rd, brampton on",
    "delivery_address": "11 church st west, Bramton On",
    "delivery_category": "CAR",
    "vehicle_type": "Car"
},
  {
    "pickup_address": "100 Innovation Drive, Toronto, ON",
    "delivery_address": "250 Tech Park, Waterloo, ON",
    "vehicle_type": "Car", 
    "delivery_category": "TECH EQUIPMENT DELIVERY"
  },
  {
    "pickup_address": "Vancouver, BC",
    "delivery_address": "Surrey, BC",
    "delivery_category": "GROCERY DELIVERY",
    "vehicle_type": "Van"
  },
  {
    "pickup_address": "Ottawa, ON",
    "delivery_address": "Montreal, QC",
    "delivery_category": "STANDARD DELIVERY",
    "vehicle_type": "Pickup Truck"
  },
  {
    "pickup_address": "Calgary, AB",
    "delivery_address": "Edmonton, AB",
    "delivery_category": "CANNABIS DELIVERY",
    "vehicle_type": "Flatbed Truck"
  },
  {
    "pickup_address": "New York, NY",
    "delivery_address": "Brooklyn, NY",
    "delivery_category": "FOOD DELIVERY",
    "vehicle_type": "Bicycle"
  }
]
```

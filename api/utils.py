import requests
import logging
from decimal import Decimal
from django.conf import settings
from urllib.parse import quote

#API Call
def fetch_nutrition_data(user_query, api_key=settings.API_KEY):
    if not user_query:
        logging.error("Empty query provided")
        return None
    
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    query_url = f"{api_url}{quote(user_query)}"
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(query_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        items = data.get("items")
        
        if items:
            processed_items = []
            for item in items:
                processed_items.append({
                    "name":          item.get("name", "Unknown").capitalize(),
                    "quantity":      Decimal(100.0),  # Default quantity is 100g
                    "calories":      Decimal(item.get("calories", 0.00)),
                    "carbohydrates": Decimal(item.get("carbohydrates_total_g", 0.00)),
                    "protein":       Decimal(item.get("protein_g", 0.00)),
                    "fat":           Decimal(item.get("fat_total_g", 0.00)),
                    "serving_size":  Decimal(item.get("serving_size_g", 0.00)),
                    "fat_saturated": Decimal(item.get("fat_saturated_g", 0.00)),
                    "sodium":        Decimal(item.get("sodium_mg", 0.00)),
                    "potassium":     Decimal(item.get("potassium_mg", 0.00)),
                    "cholesterol":   Decimal(item.get("cholesterol_mg", 0.00)),
                    "fiber":         Decimal(item.get("fiber_g", 0.00)),
                    "sugar":         Decimal(item.get("sugar_g", 0.00)),
                })
            return processed_items
        else:
            logging.warning(f"No nutrition data found for query: {user_query}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error when fetching nutrition data: {str(e)}")
        return []
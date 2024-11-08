import requests
import logging
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
            item = items[0]
            return {
                "calories": item.get("calories", 0),
                "carbohydrates": item.get("carbohydrates_total_g", 0.00),
                "protein": item.get("protein_g", 0.00),
                "fat": item.get("fat_total_g", 0.00),
            }
        else:
            logging.warning(f"No nutrition data found for query: {user_query}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error when fetching nutrition data: {str(e)}")
        return None
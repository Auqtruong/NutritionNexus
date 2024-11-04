import requests
from django.conf import settings

#API Call
def fetch_nutrition_data(user_query, api_key=settings.API_KEY):
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    query_url = f"{api_url}{user_query}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(query_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #if the food item has nutrition data to return
        if data["items"]:
            item = data["items"][0]
            return {
                "calories": item.get("calories", 0),
                "carbohydrates": item.get("carbohydrates_total_g", 0.00),
                "protein": item.get("protein_g", 0.00),
                "fat": item.get("fat_total_g", 0.00),
            }
    else:
        print(f"Error when fetching nutrition data: {response.status_code}")
        return None
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Food
from unittest.mock import patch

User = get_user_model()

class TestPaginatedFoodListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.food1  = Food.objects.create(name="Apple",  calories=52, protein=0.3, carbohydrates=14, fat=0.2)
        self.food2  = Food.objects.create(name="Banana", calories=89, protein=1.1, carbohydrates=23, fat=0.3)
        self.url    = reverse("food-list")

    def test_paginated_food_list_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], "Apple")
        self.assertEqual(response.data["results"][1]["name"], "Banana")

class TestFoodDetailView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.food   = Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2, serving_size=150)
        self.url    = reverse("food-detail", args=[self.food.id])

    def test_food_detail_success_with_default_quantity(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Apple")
        self.assertEqual(response.data["calories"], 52.0)
        
        food = Food.objects.get(id=self.food.id)
        self.assertEqual(food.protein,       round(Decimal(0.3), 1))
        self.assertEqual(food.carbohydrates, round(Decimal(14.0), 1))
        self.assertEqual(food.fat,           round(Decimal(0.2), 1))
        
    def test_food_detail_with_serving_size(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serving_size = 150
        scale_factor = Decimal(serving_size) / Decimal(100.0)

        self.assertEqual(Decimal(response.data["nutrition_per_serving"]["calories"]),       round(Decimal(52.0) * scale_factor, 1))
        self.assertEqual(Decimal(response.data["nutrition_per_serving"]["carbohydrates"]),  round(Decimal(14.0) * scale_factor, 1))
        self.assertEqual(Decimal(response.data["nutrition_per_serving"]["protein"]),        round(Decimal(0.3)  * scale_factor, 1))
        self.assertEqual(Decimal(response.data["nutrition_per_serving"]["fat"]),            round(Decimal(0.2)  * scale_factor, 1))

    def test_food_detail_not_found(self):
        url = reverse("food-detail", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestGetNutritionData(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url    = reverse("get-nutrition-data")

    @patch("api.views.fetch_nutrition_data")
    def test_get_nutrition_data_success(self, mock_fetch):
        mock_fetch.return_value = {
            "calories": 52.0,
            "carbohydrates": 14.0,
            "protein": 0.3,
            "fat": 0.2
        }
        response = self.client.get(self.url, {"food": "Apple"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["calories"], 52.0)

    def test_get_nutrition_data_no_food_query(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class TestAddFoodView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.url    = reverse("add-food")
        
    @patch("api.views.fetch_nutrition_data")
    def test_add_food_success(self, mock_fetch):
        mock_fetch.return_value = {
            "items": [
                {
                    "name": "Apple",
                    "calories": 52.0,
                    "carbohydrates_total_g": 14.0,
                    "protein_g": 0.3,
                    "fat_total_g": 0.2,
                }
            ]
        }
        
        data = {"name": "Apple"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

        apple = Food.objects.get(name="Apple")
        
        self.assertEqual(apple.calories,        round(Decimal("52.0"), 1))
        self.assertEqual(apple.carbohydrates,   round(Decimal("14.0"), 1))
        self.assertEqual(apple.protein,         round(Decimal("0.3"), 1))
        self.assertEqual(apple.fat,             round(Decimal("0.2"), 1))
        
    @patch("api.views.fetch_nutrition_data")
    def test_add_food_with_failed_nutrition_fetch(self, mock_fetch):
        mock_fetch.return_value = None
        
        data = {"name": "Peach"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertFalse(Food.objects.filter(name="Peach").exists())
        
    def test_add_food_failure_invalid_data(self):
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        
    def test_add_food_failure_duplicate_name(self):
        Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2)

        data = {"name": "Apple"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(response.data["name"][0], "A food item with this name already exists.")

class TestDeleteFoodView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.food   = Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2)
        self.url    = reverse("delete-food")

    def test_delete_food_success(self):
        response = self.client.delete(self.url, {"ids": [self.food.id]}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Food.objects.filter(id=self.food.id).exists())

    def test_delete_food_failure_no_ids(self):
        response = self.client.delete(self.url, {"ids": []}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

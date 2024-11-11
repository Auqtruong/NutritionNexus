from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Food, User
from .serializers import FoodSerializer

#User/Authenication Tests

#Food Tests
class PaginatedFoodListViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Food.objects.bulk_create([
            Food(name="Apple" , calories=53),
            Food(name="Banana", calories=100),
            Food(name="Orange", calories=50),
        ])
        
    def test_retrieve_paginated_food_list(self):
        #Test case: Retrieve paginated list of existing/saved food items
        url      = reverse("list_food_items")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        #pagination set to 10
        self.assertLessEqual(len(response.data["results"]), 10)
        
    def test_filter_food_items(self):
        #Test case: Filtering existing/saved food items based on name
        url      = reverse("list_food_items") + "?name=Apple"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Apple")

class FoodDetailViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.food = Food.objects.create(
            name="Apple", 
            calories=53,
            carbohydrates=14.1,
            protein=0.3,
            fat=0.2
        )

    def test_retrieve_specific_food_item(self):
        #Test case: Retrieve existing food item and its nutrition
        url = reverse("food_detail", args=[self.food.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Apple")
        self.assertEqual(response.data["calories"], 53)
        self.assertEqual(response.data["carbohydrates"], 14.1)
        self.assertEqual(response.data["protein"], 0.3)
        self.assertEqual(response.data["fat"], 0.2)

    def test_retrieve_non_existent_food_item(self):
        #Test case: Retrieve non-existent food item and its nutrition
        non_existent_id = self.food.pk + 1
        while Food.objects.filter(pk=non_existent_id).exists():
            non_existent_id += 1
        
        url      = reverse("food_detail", args=[non_existent_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
class AddFoodTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("add_food")
        cls.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_add_food_successful(self):
        #Test case: Add food item with valid data and successful nutrition data fetching
        with patch("api.utils.fetch_nutrition_data") as mock_fetch:
            mock_fetch.return_value = {
                "calories": 57,
                "carbohydrates": 15,
                "protein": 0.4,
                "fat": 0.1
            }
            
            data = {"name": "Pear"}
            self.client.force_authenticate(user=self.user)
            response = self.client.post(self.url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn("message", response.data)
            self.assertTrue(Food.objects.filter(name="Pear").exists())
            
            food = Food.objects.get(name="Pear")
            self.assertEqual(food.calories, 57)
            self.assertEqual(food.carbohydrates, 15)
            self.assertEqual(food.protein, 0.4)
            self.assertEqual(food.fat, 0.1)

    def test_add_food_with_failed_nutrition_fetch(self):
        #Test case: Add food item with valid data but failing nutrition data fetching
        with patch("api.utils.fetch_nutrition_data") as mock_fetch:
            mock_fetch.return_value = None
            
            data = {"name": "Peach"}
            self.client.force_authenticate(user=self.user)
            response = self.client.post(self.url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn("error", response.data)
            self.assertFalse(Food.objects.filter(name="Peach").exists())
            
    def test_add_food_with_invalid_data(self):
        #Test case: Add food item with invalid data
        data = {}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(Food.objects.count(), 0)
        
    def test_unauthentiacted_user_add_food(self):
        #Test case: Unauthenticated user attempts to add food item
        data = {"name": "Banana"}
        response = self.client.post(self.url, data, format="json")
    
        self.assertEqual(response.status_code, status=status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertFalse(Food.objects.filter(name="Banana").exists())
        
class DeleteFoodTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.food = Food.objects.create(
            name="Apple",
            calories=53
        )
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        
    def test_delete_food_item(self):
        #Test case: Delete existing food item
        url = reverse("delete_food", args=[self.food.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Food.objects.filter(pk=self.food.pk).exists())
        
    def test_delete_non_existent_food_item(self):
        #Test case: Delete non-existent food item
        non_existent_id = self.food.pk + 1
        while Food.objects.filter(pk=non_existent_id).exists():
            non_existent_id += 1
            
        url = reverse("delete_food", args=[99999])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_unauthenticated_user_delete_food_item(self):
        #Test case: Unauthorized user attempts to delete food item
        url = reverse("delete_food", args=[self.food.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(Food.objects.count(), 1)

#Daily Intake Tests

#Weight Log Tests
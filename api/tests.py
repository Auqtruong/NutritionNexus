from datetime import timedelta
from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Food, User, DailyIntake, WeightTracker
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
        url      = reverse("food_detail", args=[self.food.pk])
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
        cls.url  = reverse("add_food")
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
            
            data     = {"name": "Pear"}
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
            
            data     = {"name": "Peach"}
            self.client.force_authenticate(user=self.user)
            response = self.client.post(self.url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn("error", response.data)
            self.assertFalse(Food.objects.filter(name="Peach").exists())
            
    def test_add_food_with_invalid_data(self):
        #Test case: Add food item with invalid data
        data     = {}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(Food.objects.count(), 0)
        
    def test_unauthentiacted_user_add_food(self):
        #Test case: Unauthenticated user attempts to add food item
        data     = {"name": "Banana"}
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
        url      = reverse("delete_food", args=[self.food.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Food.objects.filter(pk=self.food.pk).exists())
        
    def test_delete_non_existent_food_item(self):
        #Test case: Delete non-existent food item
        non_existent_id = self.food.pk + 1
        while Food.objects.filter(pk=non_existent_id).exists():
            non_existent_id += 1
            
        url      = reverse("delete_food", args=[99999])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_unauthenticated_user_delete_food_item(self):
        #Test case: Unauthorized user attempts to delete food item
        url      = reverse("delete_food", args=[self.food.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(Food.objects.count(), 1)

#Daily Intake Tests
class DailyIntakeViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user        = User.objects.create_user(username="testuser", password="testpassword")
        cls.food_1      = Food.objects.create(name="Apple" , calories=53)
        cls.food_2      = Food.objects.create(name="Banana", calories=100)
        cls.food_3      = Food.objects.create(name="Orange", calories=50)
        cls.food_4      = Food.objects.create(name="Mango" , calories=75)
        cls.intake      = DailyIntake.objects.create(
                            user=cls.user,
                            food_eaten=cls.food_1,
                            food_entry_date=timezone.now().date()
                            )
        cls.list_url    = reverse("list_daily_intake")
        cls.add_url     = reverse("add_to_daily_intake")
        cls.delete_url  = reverse("delete_from_daily_intake", args=[cls.intake.id])

    def setUp(self):
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_daily_intake_for_authenticated_user(self):
        #Test case: Authorized user attempts to retrieve their Daily Intake Log
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["food"]["name"], "Apple")
        
    def test_daily_intake_filter_applied(self):
        #Test case: User attempts to filter their Daily Intake Log
        DailyIntake.objects.create(
            user=self.user,
            food_eaten=self.food_1,
            food_quantity=100,  
            food_entry_date=timezone.now().date(),
            calories=125,
            )
        DailyIntake.objects.create(
            user=self.user,
            food_eaten=self.food_2,
            food_quantity=100,
            food_entry_date=timezone.now().date() - timedelta(days=1),
            calories=75,
            )
        DailyIntake.objects.create(
            user=self.user,
            food_eaten=self.food_3,
            food_quantity=100,
            food_entry_date="2024-11-01",
            calories=100
            )
        DailyIntake.objects.create(
            user=self.user,
            food_eaten=self.food_4,
            food_quantity=100,
            food_entry_date="2024-11-05",
            calories=150
            )
        #Case 1: Filter by date range
        response = self.client.get(self.list_url + "?date_min=" + str(timezone.now().date() - timedelta(days=1)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  #Should return both entries within the date range
        
        #Case 2: Filter by date range with more constraint
        response = self.client.get(self.list_url + "?date_min=" + str(timezone.now().date()))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  #Should return only today's entries
        
        #Case 3: Filter by two specific dates
        response = self.client.get(self.list_url + "?date_min=2024-11-01&date_max=2024-11-03")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["food_eaten"]["name"], "Orange")  #Only the 2024-11-01 entry should appear
        
        #Case 4: Filter by calorie range with matching entries
        response = self.client.get(self.list_url + "?calories_min=50&calories_max=100")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["calories"], 75)
        self.assertEqual(response.data[1]["calories"], 100)
        self.assertEqual(response.data[0]["food_eaten"]["name"], "Banana")
        self.assertEqual(response.data[1]["food_eaten"]["name"], "Orange")
        
        #Case 5: Filter by calorie range with no matching entries
        response = self.client.get(self.list_url + "?calories_min=300")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  #No entries should match this range
        
        #Case 6: Filter by calories minimum only
        response = self.client.get(self.list_url + "?calories_min=100")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["calories"], 125)
        self.assertEqual(response.data[1]["calories"], 100)
        self.assertEqual(response.data[2]["calories"], 150)
        self.assertEqual(response.data[0]["food_eaten"]["name"], "Apple")
        self.assertEqual(response.data[1]["food_eaten"]["name"], "Orange")
        self.assertEqual(response.data[2]["food_eaten"]["name"], "Mango")
        
        #Case 7: Filter by calories maximum only
        response = self.client.get(self.list_url + "?calories_max=100")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["calories"], 75)
        self.assertEqual(response.data[1]["calories"], 100)
        self.assertEqual(response.data[0]["food_eaten"]["name"], "Banana")
        self.assertEqual(response.data[1]["food_eaten"]["name"], "Orange")
        
        #Case 8: Filter by both calories and date
        response = self.client.get(self.list_url + "?date_min=2024-11-01&date_max=2024-11-05&calories_min=75&calories_max=125")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["calories"], 100)
        self.assertEqual(response.data[0]["food_eaten"]["name"], "Orange")
        
    def test_retrieve_daily_intake_for_unauthenticated_user(self):
        #Test case: Unauthorized user attempts to retrieve a Daily Intake Log
        self.client.logout()
        response = self.client.get(self.list_url)
    
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_food_to_daily_intake_valid_food_id(self):
        #Test case: User attempts to add food with valid id to Daily Intake Log
        response = self.client.post(self.add_url, {"food_id": self.food_1.id, "date": timezone.now().date()}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertTrue(DailyIntake.objects.filter(user=self.user, food_eaten=self.food_1).exists())

    def test_add_food_to_daily_intake_non_existent_food_id(self):
        #Test case: User attempts to add non-existent food to Daily Intake Log
        response = self.client.post(self.add_url, {"food_id": 999999, "date": timezone.now().date()}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_add_food_to_daily_intake_unauthenticated_user(self):
        #Test case: Unauthorized user attempts to add food to Daily Intake Log
        self.client.logout()
        response = self.client.post(self.add_url, {"food_id": self.food_3.id, "date": timezone.now().date()}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_existing_daily_intake_entry(self):
        #Test case: User attempts to delete a valid entry from their Daily Intake Log
        self.assertTrue(DailyIntake.objects.filter(id=self.intake.id).exists())
        response = self.client.delete(self.delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DailyIntake.objects.filter(id=self.intake.id).exists())

    def test_delete_non_existent_daily_intake_entry(self):
        #Test case: User attempts to delete a non-existent entry from their Daily Intake Log
        non_existent_id = DailyIntake.objects.latest("id").id + 1
        url             = reverse("delete_from_daily_intake", args=[non_existent_id])
        response        = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_daily_intake_entry_unauthenticated_user(self):
        #Test case: Unauthorized user attempts to delete an entry from a Daily Intake Log
        self.client.logout()
        response = self.client.delete(self.delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
#Weight Log Tests
class WeightTrackerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user        = User.objects.create_user(username="testuser", password="testpassword")
        cls.weight_1  = WeightTracker.objects.create(user=cls.user, weight=140.00, weight_entry_date=timezone.now().date())
        cls.list_url    = reverse("list_weight_log")
        cls.record_url  = reverse("record_weight")
        cls.update_url  = reverse("update_weight_entry", args=[cls.weight_1.id])
        cls.delete_url  = reverse("delete_weight_entry", args=[cls.weight_1.id])
    
    def setUp(self):
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_weight_logs_authenticated_user(self):
        #Test case: Authenticated user retrieves their weight logs
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["weight"], "140.00")

    def test_weight_log_filter_by_date(self):
        #Create additional entries for filtering
        WeightTracker.objects.create(user=self.user, weight=200.00, weight_entry_date=timezone.now().date() - timedelta(days=2))
        WeightTracker.objects.create(user=self.user, weight=150.00, weight_entry_date="2024-10-01")

        #Case 1: Filter by date range (recent entries)
        response = self.client.get(self.list_url + "?date_min=" + str(timezone.now().date() - timedelta(days=3)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  #Should include entries within the past 3 days
        self.assertEqual(response.data[0]["weight"], "140.00")
        self.assertEqual(response.data[1]["weight"], "200.00")

        #Case 2: Filter by date range to retrieve a single specific entry
        response = self.client.get(self.list_url + "?date_min=2024-10-01&date_max=2024-10-01")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["weight"], "150.00")

    def test_weight_log_filter_by_weight(self):
        #Create additional entries for filtering
        WeightTracker.objects.create(user=self.user, weight=225.00, weight_entry_date=timezone.now().date() - timedelta(days=5))
        WeightTracker.objects.create(user=self.user, weight=125.00, weight_entry_date="2024-10-10")

        #Case 1: Filter by weight range
        response = self.client.get(self.list_url + "?weight_min=100&weight_max=155")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["weight"], "140.00")
        self.assertEqual(response.data[1]["weight"], "125.00")

        #Case 2: Filter by minimum weight only
        response = self.client.get(self.list_url + "?weight_min=155")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["weight"], "225.00")

    def test_record_weight_valid(self):
        #Test case: User attempts to record a new valid weight entry
        response = self.client.post(self.record_url, {"weight": 165.00, "date": timezone.now().date()}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertTrue(WeightTracker.objects.filter(user=self.user, weight=165.00).exists())

    def test_record_weight_invalid(self):
        #Test case: User attempts to record an invalid weight entry
        response = self.client.post(self.record_url, {"weight": "invalid_weight"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_existing_weight_entry(self):
        #Test case: User attempts to update a valid weight entry
        response = self.client.put(self.update_url, {"weight": 155.00, "date": timezone.now().date()}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Weight entry updated successfully")
        self.weight_1.refresh_from_db() #Refresh to check if entry has been updated correctly
        self.assertEqual(self.weight_1.weight, 155.00)

    def test_update_non_existent_weight_entry(self):
        #Test case: User attempts to update a non-existent weight entry
        non_existent_id = WeightTracker.objects.latest("id").id + 1
        url = reverse("update_weight_entry", args=[non_existent_id])
        response = self.client.put(url, {"weight": 145.00}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_existing_weight_entry(self):
        #Test case: User attempts to delete a valid weight entry
        response = self.client.delete(self.delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WeightTracker.objects.filter(id=self.weight_1.id).exists())

    def test_delete_non_existent_weight_entry(self):
        #Test case: User attempts to delete a non-existent weight entry
        non_existent_id = WeightTracker.objects.latest("id").id + 1
        url = reverse("delete_weight_entry", args=[non_existent_id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_unauthenticated_access(self):
        #Test case: Unauthenticated user tries to access endpoints
        self.client.logout()
        
        #Case 1: GET/Read Endpoint
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #Case 2: POST/Create Endpoint
        response = self.client.post(self.record_url, {"weight": 150.00, "date": timezone.now().date()}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #Case 3: PUT/Update Endpoint
        response = self.client.put(self.update_url, {"weight": 145.00}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        #Case 4: DELETE Endpoint
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
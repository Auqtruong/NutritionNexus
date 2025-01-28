from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Food, DailyIntake

User = get_user_model()

class TestDailyIntakeListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.food   = Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2)
        self.intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food, food_quantity=100, food_entry_date=timezone.now().date())
        self.url    = reverse("daily-intake-list")

    def test_daily_intake_list_success_current_date(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["food_eaten"]["name"], "Apple")

    def test_daily_intake_list_success_empty_for_other_date(self):
        response = self.client.get(self.url, {"food_entry_date": (timezone.now().date() - timezone.timedelta(days=1)).isoformat()})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

class TestAddToDailyIntake(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.food   = Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2)
        self.url    = reverse("add-to-daily-intake")
        self.data   = {"food_id": self.food.id, "food_quantity": 150, "date": timezone.now().date().isoformat()}

    def test_add_to_daily_intake_success(self):
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

        intake = DailyIntake.objects.get(user=self.user, food_eaten=self.food)
        
        self.assertEqual(intake.food_quantity, Decimal(150))
        self.assertEqual(intake.food_entry_date.isoformat(), self.data["date"])
        
    def test_add_to_daily_intake_success_missing_date(self):
        del self.data["date"]
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

        intake = DailyIntake.objects.get(user=self.user, food_eaten=self.food)
        
        self.assertEqual(intake.food_quantity, Decimal(150))
        self.assertEqual(intake.food_entry_date, timezone.now().date())

    def test_add_to_daily_intake_failure_invalid_food_id(self):
        self.data["food_id"] = 999
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_add_to_daily_intake_failure_missing_food_id(self):
        del self.data["food_id"]
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_to_daily_intake_failure_zero_or_negative_quantity(self):
        for quantity in [0, -50]:
            self.data["food_quantity"] = quantity
            response = self.client.post(self.url, self.data, format="json")

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)
            
    def test_add_to_daily_intake_failure_exceeding_quantity_limit(self):
        self.data["food_quantity"] = 1500
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class TestDeleteFromDailyIntake(TestCase):
    def setUp(self):
        self.client       = APIClient()
        self.user         = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.food         = Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2)
        self.intake1      = DailyIntake.objects.create(user=self.user, food_eaten=self.food, food_quantity=100, food_entry_date=timezone.now().date())
        self.intake2      = DailyIntake.objects.create(user=self.user, food_eaten=self.food, food_quantity=50, food_entry_date=(timezone.now().date() - timezone.timedelta(days=1)))
        self.other_user   = User.objects.create_user(username="otheruser", password="password")
        self.other_intake = DailyIntake.objects.create(user=self.other_user, food_eaten=self.food, food_quantity=100, food_entry_date=timezone.now().date())
        self.url          = reverse("delete-from-daily-intake")
        self.data         = {"ids": [self.intake1.id]}

    def test_delete_from_daily_intake_success(self):
        response = self.client.delete(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertFalse(DailyIntake.objects.filter(id=self.intake1.id).exists())
        
    def test_delete_from_daily_intake_success_multiple_ids(self):
        self.data["ids"] = [self.intake1.id, self.intake2.id]
        response = self.client.delete(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertFalse(DailyIntake.objects.filter(id=self.intake1.id).exists())
        self.assertFalse(DailyIntake.objects.filter(id=self.intake2.id).exists())

    def test_delete_from_daily_intake_failure_invalid_id(self):
        self.data["ids"] = [999]
        response = self.client.delete(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_from_daily_intake_failure_no_ids_provided(self):
        self.data["ids"] = []
        response = self.client.delete(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
    def test_delete_from_daily_intake_failure_other_user_entry(self):
        self.data["ids"] = [self.other_intake.id]
        response = self.client.delete(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(DailyIntake.objects.filter(id=self.other_intake.id).exists())


from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from api.models import Food, DailyIntake, WeightTracker

User = get_user_model()

class TestDashboardView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("dashboard")
        self.today = now().date()
        self.food1 = Food.objects.create(name="Apple", calories=52, protein=0.3, carbohydrates=14, fat=0.2)
        self.food2 = Food.objects.create(name="Banana", calories=89, protein=1.1, carbohydrates=23, fat=0.3)
        self.food3 = Food.objects.create(name="Steak", calories=200, protein=25, carbohydrates=0, fat=10)
        self.intake1 = DailyIntake.objects.create(user=self.user, food_eaten=self.food1, food_quantity=100, food_entry_date=self.today)
        self.intake2 = DailyIntake.objects.create(user=self.user, food_eaten=self.food2, food_quantity=100, food_entry_date=self.today)
        self.intake3 = DailyIntake.objects.create(user=self.other_user, food_eaten=self.food3, food_quantity=100, food_entry_date=self.today)

        self.old_weight = WeightTracker.objects.create(user=self.user, weight=70.0, weight_entry_date=self.today - timedelta(days=5))
        self.latest_weight = WeightTracker.objects.create(user=self.user, weight=68.5, weight_entry_date=self.today)
    
    def test_dashboard_success(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_cals"], Decimal("141"))
        self.assertEqual(response.data["total_carbs"], Decimal("37"))
        self.assertEqual(response.data["total_protein"], Decimal("1.4"))
        self.assertEqual(response.data["total_fat"], Decimal("0.5"))
    
    def test_dashboard_success_latest_weight_record(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["last_rec_weight"], Decimal("68.5"))
        self.assertEqual(response.data["last_weight_date"], self.today)
    
    def test_dashboard_failure_unauthenticated_request(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_dashboard_success_no_daily_intake_entries(self):
        DailyIntake.objects.all().delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_cals"], Decimal("0"))
        self.assertEqual(response.data["total_carbs"], Decimal("0"))
        self.assertEqual(response.data["total_protein"], Decimal("0"))
        self.assertEqual(response.data["total_fat"], Decimal("0"))
    
    def test_dashboard_success_no_weight_records(self):
        WeightTracker.objects.all().delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["last_rec_weight"])
        self.assertIsNone(response.data["last_weight_date"])
    
    def test_dashboard_success_no_data_leakage_from_other_users(self):
        WeightTracker.objects.create(user=self.other_user, weight=80.0, weight_entry_date=self.today)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_cals"], Decimal("141"))
        self.assertEqual(response.data["total_carbs"], Decimal("37"))
        self.assertEqual(response.data["total_protein"], Decimal("1.4"))
        self.assertEqual(response.data["total_fat"], Decimal("0.5"))
        self.assertEqual(response.data["last_rec_weight"], Decimal("68.5"))
        
    def test_dashboard_failure_cannot_record_future_weight(self):
        future_date = self.today + timedelta(days=6)
        response = self.client.post(reverse("record-weight"), {"weight": 75, "date": future_date}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Date must be between", response.data["error"][0])


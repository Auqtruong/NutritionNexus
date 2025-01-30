from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import WeightTracker
from datetime import date, timedelta

User = get_user_model()

class TestWeightLogListView(TestCase):
    def setUp(self):
        self.client     = APIClient()
        self.user       = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="otheruser", password="password")
        self.weight1    = WeightTracker.objects.create(user=self.user, weight=70.5, weight_entry_date=date(2025, 1, 1))
        self.weight2    = WeightTracker.objects.create(user=self.user, weight=71.0, weight_entry_date=date(2025, 1, 2))
        self.weight3    = WeightTracker.objects.create(user=self.other_user, weight=80.0, weight_entry_date=date(2025, 1, 1))
        self.url        = reverse("weight-list")
        self.client.force_authenticate(user=self.user)
        self.base_date  = date(2024, 1, 1)

    def test_fetch_weight_logs_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["weight"], f"{self.weight2.weight:.1f}")
        self.assertEqual(response.data["results"][1]["weight"], f"{self.weight1.weight:.1f}")

    def test_fetch_weight_logs_success_filtered_by_date(self):
        response = self.client.get(self.url, {"weight_entry_date": "2025-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["weight"], str(self.weight1.weight))
        
    def test_fetch_weight_logs_success_empty_logs(self):
        WeightTracker.objects.filter(user=self.user).delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])
        
    def test_fetch_weight_logs_success_pagination(self):
        for i in range(30):
            WeightTracker.objects.create(user=self.user, weight=70 + i, weight_entry_date=self.base_date + timedelta(days=i))
        response = self.client.get(self.url, {"page": 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("count", response.data)

class TestRecordWeight(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.url    = reverse("record-weight")
        self.valid_data          = {"weight": 72.5, "date": "2025-01-03"}
        self.invalid_weight_data = {"weight": "invalid", "date": "2025-01-03"}
        self.missing_data        = {"date": "2025-01-03"}

    def test_record_weight_success(self):
        response = self.client.post(self.url, self.valid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Weight recorded successfully")
        self.assertTrue(WeightTracker.objects.filter(user=self.user, weight=self.valid_data["weight"], weight_entry_date=self.valid_data["date"]).exists())

    def test_record_weight_failure_invalid_weights(self):
        invalid_weights = ["abc", -10, 1000.1]
        for weight in invalid_weights:
            response = self.client.post(self.url, {"weight": weight, "date": "2025-01-15"}, format="json")
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)

    def test_record_weight_failure_missing_data(self):
        response = self.client.post(self.url, self.missing_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"][0], "Weight is required.")

    def test_record_weight_failure_invalid_dates(self):
        invalid_dates = ["2025-02-30", "1900-01-01", "2100-01-01"]
        for date_value in invalid_dates:
            response = self.client.post(self.url, {"weight": 72.5, "date": date_value}, format="json")
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)
            
            if "1900-01-01" in date_value or "2100-01-01" in date_value:
                self.assertIn("Date must be between", response.data["error"][0])
            elif "2025-02-30" in date_value:
                self.assertIn("Invalid date", response.data["error"][0])

    def test_record_weight_failure_duplicate_weight_creation(self):
        response1 = self.client.post(self.url, {"weight": 72.5, "date": "2025-01-03"}, format="json")
        response2 = self.client.post(self.url, {"weight": 72.5, "date": "2025-01-03"}, format="json")
        
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_record_weight_failure_missing_weight(self):
        response = self.client.post(self.url, {"date": "2025-01-15"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class TestUpdateWeight(TestCase):
    def setUp(self):
        self.client       = APIClient()
        self.user         = User.objects.create_user(username="testuser", password="password")
        self.other_user   = User.objects.create_user(username="otheruser", password="password")
        self.weight_entry = WeightTracker.objects.create(user=self.user, weight=70.5, weight_entry_date="2025-01-01")
        self.url          = reverse("update-weight", args=[self.weight_entry.id])
        self.client.force_authenticate(user=self.user)
        self.valid_update_data      = {"weight": 72.0, "date": "2025-01-02"}
        self.invalid_weight_data    = {"weight": "invalid"}
        self.nonexistent_entry_url  = reverse("update-weight", args=[999])

    def test_update_weight_success(self):
        response = self.client.put(self.url, self.valid_update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        self.weight_entry.refresh_from_db()
        
        self.assertEqual(self.weight_entry.weight, self.valid_update_data["weight"])
        self.assertEqual(self.weight_entry.weight_entry_date, date(2025, 1, 2))
        
    def test_update_weight_success_partial_update_with_missing_fields(self):
        response = self.client.put(self.url, {"date": "2025-01-02"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.weight_entry.refresh_from_db()
        
        self.assertEqual(self.weight_entry.weight, 70.5)
        self.assertEqual(self.weight_entry.weight_entry_date, date(2025, 1, 2))

    def test_update_weight_failure_invalid_weight(self):
        response = self.client.put(self.url, self.invalid_weight_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_weight_failure_nonexistent_entry(self):
        response = self.client.put(self.nonexistent_entry_url, {"weight": 75.0}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        
    def test_update_weight_failure_duplicate_date(self):
        WeightTracker.objects.create(user=self.user, weight=75.0, weight_entry_date="2024-01-02")
        response = self.client.put(self.url, {"weight": 72.0, "date": "2024-01-02"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class TestDeleteWeight(TestCase):
    def setUp(self):
        self.client       = APIClient()
        self.user         = User.objects.create_user(username="testuser", password="password")
        self.weight_entry = WeightTracker.objects.create(user=self.user, weight=70.5, weight_entry_date="2025-01-01")
        self.url          = reverse("delete-weight")
        self.client.force_authenticate(user=self.user)
        self.valid_delete_data   = {"ids": [self.weight_entry.id]}
        self.no_ids_data         = {"ids": []}
        self.nonexistent_id_data = {"ids": [999]}
        self.invalid_id          = 999

    def test_delete_weight_success(self):
        response = self.client.delete(self.url, self.valid_delete_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertFalse(WeightTracker.objects.filter(id=self.weight_entry.id).exists())
        
    def test_delete_weight_success_mixed_delete_mixed_ids(self):
        response = self.client.delete(self.url, {"ids": [self.weight_entry.id, self.invalid_id]}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("invalid_ids", response.data)
        self.assertFalse(WeightTracker.objects.filter(id=self.weight_entry.id).exists())

    def test_delete_weight_failure_no_ids(self):
        response = self.client.delete(self.url, self.no_ids_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_delete_weight_failure_nonexistent_id(self):
        response = self.client.delete(self.url, self.nonexistent_id_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Deleted 0 weight entries successfully")
        self.assertTrue("invalid_ids" in response.data)
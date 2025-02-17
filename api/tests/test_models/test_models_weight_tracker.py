from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from datetime import date, timedelta
from django.utils import timezone
from api.models import User
from api.models import WeightTracker

class WeightTrackerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="securepassword123")

    def test_weight_tracker_model_success_valid_weight(self):
        entry = WeightTracker.objects.create(user=self.user, weight=70.5, weight_entry_date=date.today())
        
        self.assertEqual(entry.weight, Decimal("70.5"))
        
    def test_weight_tracker_model_success_weight_rounding(self):
        entry = WeightTracker(user=self.user, weight=75.678, weight_entry_date=date.today())
        entry.save()
        
        self.assertEqual(entry.weight, Decimal("75.7"))

    def test_weight_tracker_model_success_boundary_values(self):
        min_entry = WeightTracker(user=self.user, weight=1.0, weight_entry_date=date.today())
        max_entry = WeightTracker(user=self.user, weight=500.0, weight_entry_date=date.today() - timedelta(days=1))
        min_entry.save()
        max_entry.save()
        
        self.assertEqual(min_entry.weight, Decimal("1.0"))
        self.assertEqual(max_entry.weight, Decimal("500.0"))

    def test_weight_tracker_model_success_default_weight_entry_date(self):
        entry = WeightTracker.objects.create(user=self.user, weight=80.0)
        
        self.assertEqual(entry.weight_entry_date, date.today())

    def test_weight_tracker_model_success_bulk_deletion_performance(self):
        entries = [WeightTracker(user=self.user, weight=70.0, weight_entry_date=date.today() - timedelta(days=i)) for i in range(100)]
        WeightTracker.objects.bulk_create(entries)
        WeightTracker.objects.filter(user=self.user).delete()
        
        self.assertEqual(WeightTracker.objects.filter(user=self.user).count(), 0)
        
    def test_weight_tracker_model_success_string_input_conversion(self):
        entry = WeightTracker(user=self.user, weight="68.5", weight_entry_date=str(date.today()))
        entry.save()
        
        self.assertEqual(entry.weight, Decimal("68.5"))
        
    def test_weight_tracker_model_success_str_representation(self):
        entry = WeightTracker.objects.create(user=self.user, weight=73.2, weight_entry_date=date.today())
        
        self.assertEqual(str(entry), f"{self.user.username} - 73.2 lbs on {date.today()}")
        
    def test_weight_tracker_model_failure_negative_weight(self):
        entry = WeightTracker(user=self.user, weight=-5.0, weight_entry_date=date.today())
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Ensure this value is greater than or equal to 1.0", str(context.exception))

    def test_weight_tracker_model_failure_weight_below_minimum(self):
        entry = WeightTracker(user=self.user, weight=0.5, weight_entry_date=date.today())
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Ensure this value is greater than or equal to 1.0", str(context.exception))

    def test_weight_tracker_model_failure_weight_above_maximum(self):
        entry = WeightTracker(user=self.user, weight=600.0, weight_entry_date=date.today())
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Ensure this value is less than or equal to 500.0", str(context.exception))
        
    def test_weight_tracker_model_failure_weight_none(self):
        entry = WeightTracker(user=self.user, weight=None, weight_entry_date=date.today())
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Weight is required", str(context.exception))

    def test_weight_tracker_model_failure_max_digits_exceeded(self):
        with self.assertRaises(ValidationError) as context:
            WeightTracker.objects.create(user=self.user, weight=158.26735, weight_entry_date=date.today())
            
        self.assertIn("Ensure that there are no more than 6 digits in total.", str(context.exception))
        
    def test_weight_tracker_model_failure_invalid_date_format(self):
        entry = WeightTracker(user=self.user, weight=70.0, weight_entry_date="2023/12/31")
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn(f"Time data '{entry.weight_entry_date}' does not match format '%y-%m-%d'", str(context.exception))

    def test_weight_tracker_model_failure_future_weight_entry_date(self):
        future_date = date.today() + timedelta(days=1)
        entry = WeightTracker(user=self.user, weight=75.0, weight_entry_date=future_date)
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Date must be between", str(context.exception))

    def test_weight_tracker_model_failure_too_old_weight_entry_date(self):
        old_date = date(1999, 12, 31)
        entry = WeightTracker(user=self.user, weight=75.0, weight_entry_date=old_date)
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Date must be between", str(context.exception))

    def test_weight_tracker_model_failure_duplicate_weight_entry_date(self):
        WeightTracker.objects.create(user=self.user, weight=70.0, weight_entry_date=date.today())
        duplicate_entry = WeightTracker(user=self.user, weight=72.0, weight_entry_date=date.today())
        
        with self.assertRaises(IntegrityError) as context:
            duplicate_entry.save()
            
        self.assertIn("UNIQUE constraint failed", str(context.exception))

    def test_weight_tracker_model_failure_nonexistent_date(self):
        entry = WeightTracker(user=self.user, weight=70.0, weight_entry_date="2023-02-30")
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Day is out of range for month", str(context.exception))

    def test_weight_tracker_model_failure_invalid_weight_string(self):
        entry = WeightTracker(user=self.user, weight="seventy", weight_entry_date=date.today())
        with self.assertRaises(ValidationError) as context:
            entry.save()
            
        self.assertIn("Invalid weight format", str(context.exception))

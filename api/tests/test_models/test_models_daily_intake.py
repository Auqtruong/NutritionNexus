from decimal import ROUND_HALF_UP, Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from api.models import Food, DailyIntake

User = get_user_model()

class TestDailyIntakeModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="securepassword123")
        self.food = Food.objects.create(
            name="Apple",
            calories=Decimal("52.0"),
            quantity=Decimal("100.0"),
            carbohydrates=Decimal("14.0"),
            protein=Decimal("0.3"),
            fat=Decimal("0.2"),
        )

        self.intake = DailyIntake.objects.create(
            user=self.user,
            food_quantity=Decimal("50.0"),
            food_eaten=self.food,
            food_entry_date=timezone.now().date(),
        )
		
    def test_default_food_quantity(self):
        intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food)

        self.assertEqual(intake.food_quantity, Decimal("100.0"))
    
    def test_food_quantity_constraints(self):
        with self.assertRaises(ValidationError) as context:
            intake = DailyIntake(
                user=self.user, 
                food_eaten=self.food, 
                food_quantity=Decimal("0.5")
            )
            intake.save()
            
        self.assertIn("Ensure this value is greater than or equal to 1.0.", str(context.exception))
            
        with self.assertRaises(ValidationError) as context:
            intake = DailyIntake(
                user=self.user, 
                food_eaten=self.food, 
                food_quantity=Decimal("1001")
            )
            intake.save()
            
        self.assertIn("Ensure this value is less than or equal to 1000.0.", str(context.exception))
    
    def test_nutrition_calculation_on_save(self):
        intake = DailyIntake.objects.create(
            user=self.user, 
            food_eaten=self.food, 
            food_quantity=Decimal("50.0")
        )
        
        self.assertEqual(intake.calories, Decimal("26.0"))
        self.assertEqual(intake.carbohydrates, Decimal("7.0"))
        self.assertEqual(intake.protein, Decimal("0.2"))
        self.assertEqual(intake.fat, Decimal("0.1"))
    
    def test_default_food_entry_date(self):
        intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food)
        
        self.assertEqual(intake.food_entry_date, timezone.now().date())
    
    def test_ordering_by_date(self):
        older_intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food, food_entry_date=timezone.now().date() - timezone.timedelta(days=1))
        
        self.assertEqual(DailyIntake.objects.first(), self.intake)
        self.assertEqual(DailyIntake.objects.last(), older_intake)
    
    def test_str_representation(self):
        self.assertEqual(str(self.intake), f"{self.user.username} - {self.food.name}")
    
    def test_deletion_behavior(self):
        self.intake.delete()
        with self.assertRaises(DailyIntake.DoesNotExist):
            self.intake.refresh_from_db()
			
    def test_default_and_null_values(self):
        food   = Food.objects.create(name="Orange")
        intake = DailyIntake.objects.create(user=self.user, food_eaten=food)
        
        self.assertEqual(intake.food_quantity, Decimal("100.0"))
        self.assertEqual(intake.calories, Decimal("0.0"))
        self.assertEqual(intake.carbohydrates, Decimal("0.0"))
        self.assertEqual(intake.protein, Decimal("0.0"))
        self.assertEqual(intake.fat, Decimal("0.0"))

    def test_negative_values(self):
        with self.assertRaises(ValidationError) as context:
            intake = DailyIntake(
                user=self.user,
                food_eaten=self.food,
                food_quantity=Decimal("-100.0"),
            )
            intake.full_clean()

        self.assertIn("Ensure this value is greater than or equal to 1.0.", str(context.exception))
    
    def test_macronutrient_calculation(self):
        test_quantities = [1, 1.5, 99.9, 100, 200.1, 500, 750.3, 1000]
    
        for quantity in test_quantities:
            test_quantities = [1, 1.5, 99.9, 100, 200.1, 500, 750.3, 1000]
    
        for quantity in test_quantities:
            # Ensure `food_quantity` respects max_digits & decimal_places
            quantity_decimal = Decimal(str(quantity)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            
            intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food, food_quantity=quantity_decimal)
            
            expected_calories      = (self.food.calories      * (quantity_decimal / self.food.quantity)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            expected_carbohydrates = (self.food.carbohydrates * (quantity_decimal / self.food.quantity)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            expected_protein       = (self.food.protein       * (quantity_decimal / self.food.quantity)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            expected_fat           = (self.food.fat           * (quantity_decimal / self.food.quantity)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

            self.assertEqual(intake.calories, expected_calories)
            self.assertEqual(intake.carbohydrates, expected_carbohydrates)
            self.assertEqual(intake.protein, expected_protein)
            self.assertEqual(intake.fat, expected_fat)
    
    def test_cascade_deletion_food(self):
        intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food)
        self.food.delete()
        
        with self.assertRaises(DailyIntake.DoesNotExist):
            intake.refresh_from_db()

    def test_cascade_deletion_user(self):
        intake = DailyIntake.objects.create(user=self.user, food_eaten=self.food)
        self.user.delete()
        
        with self.assertRaises(DailyIntake.DoesNotExist):
            intake.refresh_from_db()
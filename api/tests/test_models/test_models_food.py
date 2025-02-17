from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from api.models import Food, DailyIntake

User = get_user_model()

class TestFoodModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="securepassword123")
        self.food = Food.objects.create(
            name="Apple",
            quantity=Decimal("100.0"),
            calories=Decimal("52.0"),
            carbohydrates=Decimal("14.0"),
            protein=Decimal("0.3"),
            fat=Decimal("0.2"),
        )
        self.intake = DailyIntake.objects.create(
            user=self.user,
            food_eaten=self.food,
            food_quantity=Decimal("100.0"),
            food_entry_date=timezone.now(),
        )

    def test_max_length_of_name(self):
        long_name = "A" * 76  #Max length of 75
        food = Food(name=long_name)
        with self.assertRaises(ValidationError):
            food.full_clean()

    def test_case_insensitivity_for_name_uniqueness(self):
        duplicate_food = Food(
            name="apple",
            quantity=Decimal("100.0"),
            calories=Decimal("52.0"),
            carbohydrates=Decimal("14.0"),
            protein=Decimal("0.3"),
            fat=Decimal("0.2"),
        )

        with self.assertRaises(ValidationError) as error:
            duplicate_food.save()
            
        self.assertIn("A food item with this name already exists.", error.exception.message_dict["name"])

    def test_case_insensitivity_for_external_api_query(self):
        self.assertEqual(Food.objects.filter(name__iexact="APPLE").exists(), True)
        self.assertEqual(Food.objects.filter(name__iexact="apple").exists(), True)

    def test_decimal_precision_for_nutritional_values(self):
        food = Food.objects.create(
            name="PrecisionTest",
            quantity=Decimal("100.0"),
            calories=Decimal("1.9999"),
            carbohydrates=Decimal("2.5555"),
            protein=Decimal("3.4444"),
            fat=Decimal("4.6666"),
        )
        
        self.assertEqual(food.calories, Decimal("2.0"))
        self.assertEqual(food.carbohydrates, Decimal("2.6"))
        self.assertEqual(food.protein, Decimal("3.4"))
        self.assertEqual(food.fat, Decimal("4.7"))

    def test_deletion_behavior(self):
        self.food.delete()
        with self.assertRaises(DailyIntake.DoesNotExist):
            self.intake.refresh_from_db()

    def test_null_and_default_values(self):
        food = Food.objects.create(name="Test Food")
        
        self.assertEqual(food.quantity, Decimal("100.0"))
        self.assertEqual(food.calories, Decimal("0.0"))
        self.assertEqual(food.carbohydrates, Decimal("0.0"))
        self.assertEqual(food.protein, Decimal("0.0"))
        self.assertEqual(food.fat, Decimal("0.0"))

    def test_bulk_creation_performance(self):
        foods = [
            Food(name=f"Food {i}", quantity=Decimal("100.0"), calories=Decimal("50.0"))
            for i in range(100)
        ]
        Food.objects.bulk_create(foods)
        
        self.assertEqual(Food.objects.count(), 101)
        
    def test_calculate_nutrition_for_quantity(self):
        result = self.food.calculate_nutrition_for_quantity(50)
        
        self.assertEqual(result["calories"], Decimal("26.0"))
        self.assertEqual(result["carbohydrates"], Decimal("7.0"))
        self.assertEqual(result["protein"], Decimal("0.2"))
        self.assertEqual(result["fat"], Decimal("0.1"))

        zero_result = self.food.calculate_nutrition_for_quantity(0)
        
        self.assertEqual(zero_result["calories"], Decimal("0"))
        self.assertEqual(zero_result["carbohydrates"], Decimal("0"))
        self.assertEqual(zero_result["protein"], Decimal("0"))
        self.assertEqual(zero_result["fat"], Decimal("0"))

    def test_calculate_nutrition_for_serving_size(self):
        self.food.serving_size = Decimal("50.0")
        result = self.food.calculate_nutrition_for_serving_size()
        
        self.assertEqual(result["calories"], Decimal("26.0"))
        self.assertEqual(result["carbohydrates"], Decimal("7.0"))
        self.assertEqual(result["protein"], Decimal("0.2"))
        self.assertEqual(result["fat"], Decimal("0.1"))

        self.food.serving_size = None
        null_result = self.food.calculate_nutrition_for_serving_size()
        
        self.assertIsNone(null_result["calories"])
        self.assertIsNone(null_result["carbohydrates"])
        self.assertIsNone(null_result["protein"])
        self.assertIsNone(null_result["fat"])

    def test_clean_method_name_stripping_and_title_case(self):
        food = Food(name="  banana  ")
        food.clean()
        
        self.assertEqual(food.name, "Banana")

    def test_clean_method_rounding(self):
        food = Food(
            name="RoundedTest",
            quantity=Decimal("100.0"),
            calories=Decimal("3.555"),
            carbohydrates=Decimal("6.444"),
            protein=Decimal("7.499"),
            fat=Decimal("9.666"),
        )
        food.clean()
        
        self.assertEqual(food.calories, Decimal("3.6"))
        self.assertEqual(food.carbohydrates, Decimal("6.4"))
        self.assertEqual(food.protein, Decimal("7.5"))
        self.assertEqual(food.fat, Decimal("9.7"))

    def test_save_calls_clean(self):
        food = Food.objects.create(
            name="  orange  ",
            quantity=Decimal("100.0"),
            calories=Decimal("3.555"),
        )
        
        self.assertEqual(food.name, "Orange")
        self.assertEqual(food.calories, Decimal("3.6"))

    def test_negative_values(self):
        with self.assertRaises(ValidationError) as context:
            food = Food(
                name="Extreme",
                quantity=Decimal("-503.9"),
                calories=Decimal("-99999.9"),
                carbohydrates=Decimal("-1.0"),
                protein=Decimal("-0.0001"),
                fat=Decimal("100.999"),
            )
            food.save()
            
        self.assertIn("Ensure this value is greater than or equal to 0.0.", str(context.exception))
        
    def test_max_digits_constraint(self):
        with self.assertRaises(ValidationError) as context:
            Food.objects.create(
                name="ExceedMaxDigits",
                quantity=Decimal("1000000.0"),
                calories=Decimal("999999.9"),
                carbohydrates=Decimal("100000.0"), 
                protein=Decimal("99999.9"),
                fat=Decimal("100000.0"),
            )
            
        self.assertIn("Ensure that there are no more than 6 digits in total.", str(context.exception))
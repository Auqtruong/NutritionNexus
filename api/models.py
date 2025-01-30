from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
# User Model
class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        default="profile_pictures/default.jpg", #default profile picture for all users
    )

    def __str__(self):
        return f'{self.username}'

    class Meta:
        # Meta options for your model
        verbose_name = "User"
        verbose_name_plural = "Users"

    
#Food/Macros Model
class Food(models.Model):
    name            = models.CharField(max_length=75, unique=True)
    quantity        = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(100.0))
    calories        = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    carbohydrates   = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    protein         = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    fat             = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    
    serving_size    = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #g
    fat_saturated   = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #g
    sodium          = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #mg
    potassium       = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #mg
    cholesterol     = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #mg
    fiber           = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #g
    sugar           = models.DecimalField(max_digits=6, decimal_places=1, default=None, null=True, blank=True) #g
    #category for food types?
    
    #calculate calories/macros based on quantity of food entry
    def calculate_nutrition_for_quantity(self, quantity):
        if self.quantity == 0:
            return {field: 0 for field in [
                "calories",
                "carbohydrates",
                "protein",
                "fat",
                "fat_saturated",
                "sodium",
                "potassium",
                "cholesterol",
                "fiber",
                "sugar"
            ]}
        
        amount = Decimal(str(quantity)) / Decimal(str(self.quantity))
        return {
            "calories":      Decimal(self.calories      * amount),
            "carbohydrates": Decimal(self.carbohydrates * amount),
            "protein":       Decimal(self.protein       * amount),
            "fat":           Decimal(self.fat           * amount),
            "fat_saturated": Decimal((self.fat_saturated or 0) * amount),
            "sodium":        Decimal((self.sodium        or 0) * amount),
            "potassium":     Decimal((self.potassium     or 0) * amount),
            "cholesterol":   Decimal((self.cholesterol   or 0) * amount),
            "fiber":         Decimal((self.fiber         or 0) * amount),
            "sugar":         Decimal((self.sugar         or 0) * amount),
        }
        
    #calculate nutrition for 1 serving of food item
    def calculate_nutrition_for_serving_size(self):
        if not self.serving_size or self.quantity == 0:
            return {field: None for field in [
                "calories",
                "carbohydrates",
                "protein",
                "fat",
                "fat_saturated",
                "sodium",
                "potassium",
                "cholesterol",
                "fiber",
                "sugar"
            ]}

        amount = Decimal(str(self.serving_size)) / Decimal(100.0)
        return {
            "calories":      round(Decimal(self.calories      * amount), 1),
            "carbohydrates": round(Decimal(self.carbohydrates * amount), 1),
            "protein":       round(Decimal(self.protein       * amount), 1),
            "fat":           round(Decimal(self.fat           * amount), 1),
            "fat_saturated": round(Decimal((self.fat_saturated or 0) * amount), 1),
            "sodium":        round(Decimal((self.sodium        or 0) * amount), 1),
            "potassium":     round(Decimal((self.potassium     or 0) * amount), 1),
            "cholesterol":   round(Decimal((self.cholesterol   or 0) * amount), 1),
            "fiber":         round(Decimal((self.fiber         or 0) * amount), 1),
            "sugar":         round(Decimal((self.sugar         or 0) * amount), 1),
        }
        
    def __str__(self):
        return self.name
    
    def clean(self):
        #Ensure all relevant fields are Decimal and rounded
        fields_to_round = [
            "quantity", 
            "calories", 
            "carbohydrates", 
            "protein", 
            "fat",
            "fat_saturated",
            "sodium",
            "potassium",
            "cholesterol",
            "fiber",
            "sugar",
            "serving_size"
        ]
        for field in fields_to_round:
            value = getattr(self, field, None)
            if value is not None:
                setattr(self, field, round(Decimal(value), 1))
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["name"]   

#Daily Intake Model
class DailyIntake(models.Model):
    #delete rows in corresponding table if rows are removed here
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_intakes")
    food_eaten      = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="intakes")
    
    #100g default for food entries
    food_quantity   = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal(100.00), validators=[MinValueValidator(Decimal("1.0")), MaxValueValidator(Decimal("1000.0"))])
    food_entry_date = models.DateField(default=timezone.now)
    
    calories        = models.DecimalField(max_digits=6, decimal_places=1, editable=False, default=Decimal(0.0))
    carbohydrates   = models.DecimalField(max_digits=6, decimal_places=1, editable=False, default=Decimal(0.0))
    protein         = models.DecimalField(max_digits=6, decimal_places=1, editable=False, default=Decimal(0.0))
    fat             = models.DecimalField(max_digits=6, decimal_places=1, editable=False, default=Decimal(0.0))
    
    class Meta:
        #chronological ordering
        verbose_name        = "Daily Log"
        verbose_name_plural = "Daily Logs"
        ordering            = ["-food_entry_date"]
        
    def clean(self):
        #Ensure all relevant fields are Decimal
        self.food_quantity  = Decimal(self.food_quantity)
        self.calories       = Decimal(self.calories)
        self.carbohydrates  = Decimal(self.carbohydrates)
        self.protein        = Decimal(self.protein)
        self.fat            = Decimal(self.fat)
        
    #calculate cals/macros based on quantity manually entered; override Django save method
    def save(self, *args, **kwargs):
        self.full_clean()
        
        nutrition           = self.food_eaten.calculate_nutrition_for_quantity(self.food_quantity)
        self.calories       = nutrition["calories"]
        self.carbohydrates  = nutrition["carbohydrates"]
        self.protein        = nutrition["protein"]
        self.fat            = nutrition["fat"]
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.user.username} - {self.food_eaten.name}'

# Weight Tracker Model
class WeightTracker(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weight_logs")
    weight              = models.DecimalField(max_digits=6, decimal_places=1)
    weight_entry_date   = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name        = "Weight Log"
        verbose_name_plural = "Weight Logs"
        ordering            = ["-weight_entry_date"]
        unique_together     = ("user", "weight_entry_date")
    
    def clean(self):
        min_date = date(2000, 1, 1)
        max_date = date.today()
        
        if isinstance(self.weight, str):
            try:
                self.weight = Decimal(self.weight)
            except (ValueError, InvalidOperation):
                raise ValidationError("Invalid weight format. Please provide a valid number.")

        if isinstance(self.weight_entry_date, str):
            try:
                self.weight_entry_date = datetime.strptime(self.weight_entry_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format. Use the format YYYY-MM-DD.")

        try:
            self.weight_entry_date = date(self.weight_entry_date.year, self.weight_entry_date.month, self.weight_entry_date.day)
        except ValueError:
            raise ValidationError("The date provided does not exist. Please provide a valid date.")

        if self.weight_entry_date < min_date or self.weight_entry_date > max_date:
            raise ValidationError(f"Date must be between {min_date} and {max_date}.")

        if self.weight is None:
            raise ValidationError("Weight is required.")
        
        weight_min_validator = MinValueValidator(Decimal("1.0"))
        weight_max_validator = MaxValueValidator(Decimal("500.0"))
        
        weight_min_validator(self.weight)
        weight_max_validator(self.weight)
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.username} - {self.weight} lbs on {self.weight_entry_date}'
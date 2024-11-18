from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
#User Model
class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="api_user_set",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions_set',
    )
    
    def __str__(self):
        return f'{self.username}'
    
#Food/Macros Model
class Food(models.Model):
    name            = models.CharField(max_length=75)
    quantity        = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(100.0))
    calories        = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    carbohydrates   = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    protein         = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    fat             = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal(0.0))
    #category for food types?
    
    #calculate calories/macros based on quantity of food entry
    def calculate_nutrition_for_quantity(self, quantity):
        if self.quantity == 0:
            return {
                "calories": 0,
                "carbohydrates": 0,
                "protein": 0,
                "fat": 0
            }
        
        amount = Decimal(str(quantity)) / Decimal(str(self.quantity))
        return {
            "calories":      Decimal(self.calories * amount),
            "carbohydrates": Decimal(self.carbohydrates * amount),
            "protein":       Decimal(self.protein * amount),
            "fat":           Decimal(self.fat * amount),
        }
        
    def __str__(self):
        return self.name
    
    def clean(self):
        #Ensure all relevant fields are Decimal
        self.quantity       = round(Decimal(self.quantity), 1)
        self.calories       = round(Decimal(self.calories), 1)
        self.carbohydrates  = round(Decimal(self.carbohydrates), 1)
        self.protein        = round(Decimal(self.protein), 1)
        self.fat            = round(Decimal(self.fat), 1)
    
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
    food_quantity   = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal(100.00))
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

#Weight Tracker Model
class WeightTracker(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weight_logs")
    weight              = models.DecimalField(max_digits=6, decimal_places=2)
    weight_entry_date   = models.DateField(default=timezone.now)
    
    class Meta:
        #chronological ordering
        verbose_name        = "Weight Log"
        verbose_name_plural = "Weight Logs"
        ordering            = ["-weight_entry_date"]
    
    def __str__(self):
        return f'{self.user.username} - {self.weight} lbs on {self.weight_entry_date}'
    
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import requests

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
    quantity        = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    calories        = models.IntegerField(default=0)
    carbohydrates   = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    protein         = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    fat             = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    #category for food types?
    
    def fetch_nutrition_data(self):
        api_url = "https://api.calorieninjas.com/v1/nutrition?query="
        query = f''
        response = requests.get(api_url + query, headers={'X-Api-Key': 'YOUR_API_KEY'})
        
        if response.status_code == response.codes.ok:
            data = response.json()
            #if the food item has nutrition data to return
            if data["items"]:
                item                = data["items"][0]
                self.calories       = item.get("calories", 0)
                self.carbohydrates  = item.get("carbohydrates", 0.00)
                self.protein        = item.get("protein_g", 0.00)
                self.fat            = item.get("fat_total_g", 0.00)
                self.save()
        else:
            print(f"Error when fetching nutrition data: {response.status_code}")
                

#Daily Intake Model
class DailyIntake(models.Model):
    #delete rows in corresponding table if rows are removed here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_eaten = models.ForeignKey(Food, on_delete=models.CASCADE)
    food_entry_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Daily Log"
        verbose_name_plural = "Daily Logs"
        
    def __str__(self):
        return f'{self.user.username} - {self.food_eaten.name}'

#Weight Tracker Model
class WeightTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    weight_entry_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Weight Log"
        verbose_name_plural = "Weight Logs"
    
    def __str__(self):
        return f'{self.user.username} - {self.weight} lbs on {self.weight_entry_date}'
    

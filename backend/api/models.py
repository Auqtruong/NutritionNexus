from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#User Model
class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    
#Food/Macros Model
class Food(models.Model):
    name            = models.CharField(max_length=75)
    quantity        = models.DecimalField(max_digits=6, decimal_places=2, defualt=100.00)
    calories        = models.IntegerField(default=0)
    carbohydrates   = models.DecimalField(max_digits=6, decimal_places=2)
    protein         = models.DecimalField(max_digits=6, decimal_places=2)
    fat             = models.DecimalField(max_digits=6, decimal_places=2)
    #category for food types?

#Daily Intake Model
class DailyIntake(models.Model):
    #delete rows in corresponding table if rows are removed here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_eaten = models.ForeignKey(Food, on_delete=models.CASCADE)
    
    class Meta:
        full_name = "Daily Log"
        
    def __str__(self):
        return f'{self.user.username} - {self.food_eaten.name}'

#Weight Tracker Model
class WeightTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    weight_entry_date = models.DateField()
    
    class Meta:
        full_name = "Weight Log"
    
    def __str__(self):
        return f''
    

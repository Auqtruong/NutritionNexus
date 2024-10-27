from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Food, DailyIntake, WeightTracker

#serializers to convert python datatypes to be converted to json/xml/etc and vice-versa
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        #make password only visible on user creation, not when retieving info about the user, otherwise password will be exposed
        extra_kwargs = {"password" : {"write_only": True}}
        
    def create(self, validatedData):
        #user will be created if user data/fields are validated by previous check
        user = User.objects.create_user(**validatedData)
        return user
    
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name"]
        
class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'quantity', 'calories', 'carbohydrates', 'protein', 'fat']
        
class DailyIntakeSerializer(serializers.ModelSerializer):
    food_eaten      = FoodSerializer()
    calories        = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
    carbohydrates   = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
    protein         = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
    fat             = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
    
    class Meta:
        model = DailyIntake
        fields = ["id", "user", "food_eaten", "food_entry_date"]
        
class WeightTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightTracker
        fields = ["id", "user", "weight", "weight_entry_date"]        
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

#Serializer for paginated list of foods 
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name"]
        
#Serializer for creating new foods
class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["name", "calories", "carbohydrates", "protein", "fat"]
        
    def create(self, validated_data):
        return super().create(validated_data)
        
#Serializer for specific details (cals/macros) of a food
class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "quantity", "calories", "carbohydrates", "protein", "fat"]
        
#Serializer for a user's Daily Intake Log
class DailyIntakeSerializer(serializers.ModelSerializer):
    food_eaten      = FoodSerializer()
    calories        = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    carbohydrates   = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    protein         = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    fat             = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    
    class Meta:
        model = DailyIntake
        fields = ["id", "user", "food_eaten", "calories", "carbohydrates", "protein", "fat", "food_entry_date"]
        
#Serializer for a user's Weight Log
class WeightTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightTracker
        fields = ["id", "user", "weight", "weight_entry_date"]        
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Sum
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
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

#Serializer for paginated list of foods 
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "calories", "carbohydrates", "protein", "fat"]
        
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
        fields = ["id", "food_eaten", "calories", "carbohydrates", "protein", "fat", "food_entry_date"]
        
#Serializer for a user's Weight Log
class WeightTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightTracker
        fields = ["id", "user", "weight", "weight_entry_date"]
        
#Serializer for a user's dashboard
class DashboardSerializer(serializers.ModelSerializer):
    total_cals          = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    total_carbs         = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    total_protein       = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    total_fat           = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=1)
    last_rec_weight     = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2, allow_null=True)
    last_weight_date    = serializers.DateField(allow_null=True)
    
    def to_representation(self, instance):
        user = self.context['request'].user
        today = self.context['today']
        
        #Daily intake data
        daily_intake = DailyIntake.objects.filter(user=user, food_entry_date=today)
        totals       = daily_intake.aggregate(
                        total_cals=Sum("calories"),
                        total_carbs=Sum("carbohydrates"),
                        total_protein=Sum("protein"),
                        total_fat=Sum("fat")
                       )
        #Weight data
        last_weight = WeightTracker.objects.filter(user=user).order_by("-weight_entry_date").first()
        
        return {
            "total_cals": totals.get("total_cals") or Decimal(0),
            "total_carbs": totals.get("total_carbs") or Decimal(0),
            "total_protein": totals.get("total_protein") or Decimal(0),
            "total_fat": totals.get("total_fat") or Decimal(0),
            "last_rec_weight": last_weight.weight if last_weight else None,
            "last_weight_date": last_weight.weight_entry_date if last_weight else None,
        }
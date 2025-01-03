from datetime import date
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FoodFilter, DailyIntakeFilter, WeightLogFilter
from .serializers import FoodCreateSerializer, UserSerializer, FoodSerializer, FoodDetailSerializer, DailyIntakeSerializer, WeightTrackerSerializer, DashboardSerializer
from .models import Food, DailyIntake, WeightTracker
from .utils import fetch_nutrition_data

User = get_user_model()

#User view
class CreateUserView(CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user     = User.objects.get(username=request.data["username"])
        refresh  = RefreshToken.for_user(user)
        
        response.data["refresh"] = str(refresh)
        response.data["access"]  = str(refresh.access_token)
        return response
    
#Update user view
class UpdateUserView(UpdateAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
#Delete user view
class DeleteUserView(DestroyAPIView):
    queryset           = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


#Logout view; POST view that logs out authenticated users, returning a 200 response for success
@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token         = RefreshToken(refresh_token)
        token.blacklist() #Blacklist used tokens
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#List All Food Items View with Pagination
class PaginatedFoodListView(ListAPIView):
    queryset            = Food.objects.all()
    serializer_class    = FoodSerializer
    filter_backends     = [DjangoFilterBackend, OrderingFilter]
    filterset_class     = FoodFilter
    pagination_class    = PageNumberPagination
    ordering_fields     = ["name", "calories", "carbohydrates", "protein", "fat"]
    permission_classes  = [AllowAny]
    
#Food nutrition/details view; GETs specific food item and its info based on its Primary Key (pk)
class FoodDetailView(RetrieveAPIView):
    queryset            = Food.objects.all()
    serializer_class    = FoodDetailSerializer
    permission_classes  = [AllowAny]
    lookup_field        = "pk"
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_nutrition_data(request):
    food_query = request.query_params.get("food")
    if not food_query:
        return Response({"error": "No food item specified"}, status=status.HTTP_400_BAD_REQUEST)
    
    nutrition_data = fetch_nutrition_data(food_query)
    if nutrition_data:
        return Response(nutrition_data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to fetch nutrition data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#Add new foods to list/database of foods; return 400 if request is unsuccessful
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_food(request):
    serializer = FoodCreateSerializer(data=request.data)
    if serializer.is_valid():
        #fetch food name and nutrition data before saving
        food_name       = serializer.validated_data.get("name")
        nutrition_data  = fetch_nutrition_data(food_name)
        
        if nutrition_data and "items" in nutrition_data:
            saved_foods = []
            for item in nutrition_data["items"]:
                try:
                    food = Food.objects.create(
                        name=item["name"],
                        calories=item["calories"],
                        carbohydrates=item["carbohydrates_total_g"],
                        protein=item["protein_g"],
                        fat=item["fat_total_g"],
                        user=request.user
                    )
                    saved_foods.append(food.name)
                except Exception as e:
                    continue #Put errors here specific to saving foods
            return Response({"message": "Food items added successfully", "foods": saved_foods}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to fetch nutrition data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete existing/created foods from list/database of foods; return 204 if success, 404 if food is not found
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_food(request, pk):
    try:
        food = Food.objects.get(id=pk)
        food.delete()
        return Response({"message": "Food item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Food.DoesNotExist:
        return Response({"error": "Food item not found"}, status=status.HTTP_404_NOT_FOUND)
    
#List Daily Intake of Authenticated User
class DailyIntakeListView(ListAPIView):
    serializer_class    = DailyIntakeSerializer
    filter_backends     = [DjangoFilterBackend, OrderingFilter]
    filterset_class     = DailyIntakeFilter
    ordering_fields     = ["calories", "food_entry_date", "food_eaten__name" ]
    ordering            = ["-food_entry_date"]
    permission_classes  = [IsAuthenticated]
    
    def get_queryset(self):
        #Default display shows current date's entries; filters for other previous dates will override
        queryset = DailyIntake.objects.filter(user=self.request.user)
        
        if not self.request.query_params.get("date_min") and not self.request.query_params.get("date_max"):
            today    = date.today()
            queryset = queryset.filter(food_entry_date=today)
            
        return queryset
    
#Add Food to Daily Intake View; Must be authenticated user; Adds food item to intake based on food id
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_daily_intake(request):
    user          = request.user
    food_id       = request.data.get("food_id")
    food_quantity = Decimal(request.data.get("food_quantity", 100.00))
    
    try:
        food = Food.objects.get(id=food_id)
        DailyIntake.objects.create(
            user=user, 
            food_eaten=food,
            food_quantity=food_quantity,
            food_entry_date=request.data.get("date")
        )
        return Response({"message": f"{food.name} added to your daily intake"}, status=status.HTTP_201_CREATED)
    except Food.DoesNotExist:
        return Response({"error": "Food item not found"}, status=status.HTTP_404_NOT_FOUND)

#Delete Food from Daily Intake View; Only delete if entry is available in Daily Intake; 204 if success, 404 if unable to find food entry
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_from_daily_intake(request, pk):
    try:
        intake = DailyIntake.objects.get(id=pk, user=request.user)
        intake.delete()
        return Response({"message": "Entry deleted"}, status=status.HTTP_204_NO_CONTENT)
    except DailyIntake.DoesNotExist:
        return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
    
#List Weight Log of Authenticated User
class WeightLogListView(ListAPIView):
    queryset            = WeightTracker.objects.all()
    serializer_class    = WeightTrackerSerializer
    filter_backends     = [DjangoFilterBackend, OrderingFilter]
    filterset_class     = WeightLogFilter
    pagination_class    = PageNumberPagination
    ordering_fields     = ["weight", "weight_entry_date"]
    permission_classes  = [IsAuthenticated]
    
    def get_queryset(self):
        return WeightTracker.objects.filter(user=self.request.user)
    
#Record User Weight View; 201 if weight is sucessfully created and entered into log
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_weight(request):
    weight = request.data.get("weight")
    if not isinstance(weight, (int, float)):
        return Response({"error": "Invalid weight value"}, status=status.HTTP_400_BAD_REQUEST)
    WeightTracker.objects.create(user=request.user, weight=weight, weight_entry_date=request.data.get("date"))
    return Response({"message": "Weight recorded successfully"}, status=status.HTTP_201_CREATED)

#Update User Weight View; 200 for success, 404 if unable to find weight to update; default to existing entry if no new weight is provided
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_weight_entry(request, pk):
    try:
        weight_entry                    = WeightTracker.objects.get(id=pk, user=request.user)
        weight_entry.weight             = request.data.get("weight", weight_entry.weight)
        weight_entry.weight_entry_date  = request.data.get("date", weight_entry.weight_entry_date)
        weight_entry.save()
        return Response({"message": "Weight entry updated successfully"}, status=status.HTTP_200_OK)
    except WeightTracker.DoesNotExist:
        return Response({"error": "Weight entry not found"}, status=status.HTTP_404_NOT_FOUND)
        

#Delete a Weight Entry from User Weight Log; Only delete if entry is available in Weight Log; 204 if success, 404 if unable to find weight entry
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_weight_entry(request, pk):
    try:
        weight_entry = WeightTracker.objects.get(id=pk, user=request.user)
        weight_entry.delete()
        return Response({"message": "Weight entry deleted"}, status=status.HTTP_204_NO_CONTENT)
    except WeightTracker.DoesNotExist:
        return Response({"error": "Weight entry not found"}, status=status.HTTP_404_NOT_FOUND)
    
#Dashboard view
class DashboardView(RetrieveAPIView):
    serializer_class    = DashboardSerializer
    permission_classes  = [IsAuthenticated]
    
    def get_object(self):
        return {
            "request": self.request,
            "today": date.today()
        }
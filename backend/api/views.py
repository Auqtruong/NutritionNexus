from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FoodFilter, DailyIntakeFilter, WeightLogFilter
from .serializers import UserSerializer, FoodSerializer, FoodDetailSerializer, DailyIntakeSerializer
from .models import Food, DailyIntake, WeightTracker
# Create your views here.

#User view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
#Login view; authenticate user and allow them to login; 200 for success and 400 for failure
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

#Logout view; POST view that logs out authenticated users, returning a 200 response for success
@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout sucessful"}, status=status.HTTP_200_OK)
    
#List All Food Items View with Pagination
class PaginatedFoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FoodFilter
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    
#Food nutrition/details view; GETs specific food item and its info based on its Primary Key (pk)
class FoodDetailView(generics.RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"
    
#List Daily Intake of Authenticated User
class DailyIntakeListView(generics.ListAPIView):
    serializer_class = DailyIntakeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DailyIntakeFilter
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailyIntake.objects.filter(user=self.request.user)

#Add Food to Daily Intake View; Must be authenticated user; Adds food item to intake based on food id
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_daily_intake(request):
    user = request.user
    food_id = request.data.get("food_id")
    food = Food.objects.get(id=food_id)
    DailyIntake.objects.create(user=user, food_eaten=food, food_entry_date=request.data.get("date"))
    return Response({"message": f"{food.name} added to your daily intake"}, status=status.HTTP_201_CREATED)

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
class WeightLogListView(generics.ListAPIView):
    serializer_class = DailyIntakeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WeightLogFilter
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WeightTracker.objects.filter(user=self.request.user)
    
#Record User Weight View; 201 if weight is sucessfully created and entered into log
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_weight(request):
    weight = request.data.get("weight")
    WeightTracker.objects.create(user=request.user, weight=weight, weight_entry_date=request.data.get("date"))
    return Response({"message": "Weight recorded successfully"}, status=status.HTTP_201_CREATED)

#Delete a Weight Entry from User Weight Log; Only delete if entry is available in Weight Log; 204 if success, 404 if unable to find weight entry
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_weight_entry(request, pk):
    try:
        weight_entry = WeightTracker.objects.get(id=pk, user=request.user)
        weight_entry.delete()
        return Response({"message": "Weight entry deleted"}, status=status.HTTP_204_NO_CONTENT)
    except WeightTracker.DoesNotExist:
        return Response({"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND)
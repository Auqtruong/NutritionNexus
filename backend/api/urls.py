"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path, include

#Pre-built views to obtain access/refresh tokens and refresh those tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateUserView, DailyIntakeListView, FoodDetailView, PaginatedFoodListView, WeightLogListView
from . import views

urlpatterns = [
    #Registration/Token paths
    path("api/user/register/"   , CreateUserView.as_view()      , name="register"),
    path("api/token/"           , TokenObtainPairView.as_view() , name="get_token"),
    path("api/token/refresh/"   , TokenRefreshView.as_view()    , name="refresh_token"),
    
    #link all pre-built urls from Django REST Framework
    path("api-auth/", include("rest_framework.urls")),
    
    #Authentication paths
    path("api/login/"           , views.login_view  , name="login"),
    path("api/logout/"          , views.logout_view , name="logout"),
    
    #Food paths
    path("api/foods/"                   , PaginatedFoodListView.as_view()   , name="list_food_items"),
    path("api/foods/<int:pk>/"          , FoodDetailView.as_view()          , name="food_detail"),
    path("api/foods/add/"               , views.add_food                    , name="add_food"),
    path("api/foods/delete/<int:pk>/"   , views.delete_food                 , name="delete_food"),
    
    #Daily Intake paths
    path("api/intake/"                  , DailyIntakeListView.as_view() , name="list_daily_intake"),
    path("api/intake/add/"              , views.add_to_daily_intake     , name="add_to_daily_intake"),
    path("api/intake/delete/<int:pk>/"  , views.delete_from_daily_intake, name="delete_from_daily_intake"),
    
    #Weight Tracking paths
    path("api/weight/"                  , WeightLogListView.as_view()   , name="list_weight_log"),
    path("api/weight/record/"           , views.record_weight           , name="record_weight"),
    path("api/weight/update/<int:pk>/"  , views.update_weight_entry     , name="update_weight_entry"),
    path("api/weight/delete/<int:pk>/"  , views.delete_weight_entry     , name="delete_weight_entry"),
]

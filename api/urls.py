from django.contrib import admin
from django.urls import path, include

#Pre-built views to obtain access/refresh tokens and refresh those tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateUserView, UpdateUserView, DeleteUserView, DailyIntakeListView, FoodDetailView, PaginatedFoodListView, WeightLogListView, get_nutrition_data, DashboardView
from . import views

#API Endpoints
urlpatterns = [
    #link all pre-built urls from Django REST Framework
    path("api-auth/"                    , include("rest_framework.urls")),
    
    #Registration/Token paths
    path("api/user/register/"           , CreateUserView.as_view()          , name="register"),
    path("api/token/"                   , TokenObtainPairView.as_view()     , name="token_obtain_pair"),
    path("api/token/refresh/"           , TokenRefreshView.as_view()        , name="token_refresh"),
    
    #User paths
    path("api/user/update/"             , UpdateUserView.as_view()          , name="update-user"),
    path("api/user/delete/"             , DeleteUserView.as_view()          , name="delete-user"),
    
    #Authentication paths
    path("api/logout/"                  , views.logout_view , name="logout"),
    
    #Food paths
    path("api/foods/"                   , PaginatedFoodListView.as_view()   , name="list_food_items"),
    path("api/foods/<int:pk>/"          , FoodDetailView.as_view()          , name="food_detail"),
    path("api/foods/add/"               , views.add_food                    , name="add_food"),
    path("api/foods/delete/"            , views.delete_food                 , name="delete_food"),
    path("api/nutrition/"               , get_nutrition_data                , name="get_nutrition_data"),
    
    #Daily Intake paths
    path("api/intake/"                  , DailyIntakeListView.as_view()     , name="list_daily_intake"),
    path("api/intake/add/"              , views.add_to_daily_intake         , name="add_to_daily_intake"),
    path("api/intake/delete/"           , views.delete_from_daily_intake    , name="delete_from_daily_intake"),
    
    #Weight Tracking paths
    path("api/weight/"                  , WeightLogListView.as_view()       , name="list_weight_log"),
    path("api/weight/record/"           , views.record_weight               , name="record_weight"),
    path("api/weight/update/<int:pk>/"  , views.update_weight_entry         , name="update_weight_entry"),
    path("api/weight/delete/<int:pk>/"  , views.delete_weight_entry         , name="delete_weight_entry"),
    
    #Dashboard path
    path("api/dashboard/"               , DashboardView.as_view()           , name="dashboard")
]
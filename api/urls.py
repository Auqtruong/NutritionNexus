from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#Pre-built views to obtain access/refresh tokens and refresh those tokens
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
)
from .views import (
    CreateUserView,
    UpdateUserView,
    DeleteUserView,
    DailyIntakeListView,
    FoodDetailView,
    PaginatedFoodListView,
    UploadProfilePictureView,
    UserProfileView,
    WeightLogListView,
    get_nutrition_data,
    DashboardView
)
from . import views

#API Endpoints
urlpatterns = [
    #link all pre-built urls from Django REST Framework
    path("api-auth/"                    , include("rest_framework.urls")),
    
    #Registration/Token paths
    path("api/user/register/"               , CreateUserView.as_view()          , name="register"),
    path("api/token/"                       , TokenObtainPairView.as_view()     , name="token-obtain-pair"),
    path("api/token/refresh/"               , TokenRefreshView.as_view()        , name="token-refresh"),
    
    #User paths
    path("api/user/update/"                 , UpdateUserView.as_view()          , name="update-user"),
    path("api/user/delete/"                 , DeleteUserView.as_view()          , name="delete-user"),
    path("api/user/profile/"                , UserProfileView.as_view()         , name="user-profile"),
    path("api/user/upload-profile-picture/" , UploadProfilePictureView.as_view(), name="upload-profile-picture"),
    
    #Authentication paths
    path("api/logout/"                      , views.logout_view , name="logout"),
    
    #Food paths
    path("api/foods/"                       , PaginatedFoodListView.as_view()   , name="food-list"),
    path("api/foods/<int:pk>/"              , FoodDetailView.as_view()          , name="food-detail"),
    path("api/foods/add/"                   , views.add_food                    , name="add-food"),
    path("api/foods/delete/"                , views.delete_food                 , name="delete-food"),
    path("api/nutrition/"                   , get_nutrition_data                , name="get-nutrition-data"),
    
    #Daily Intake paths
    path("api/intake/"                      , DailyIntakeListView.as_view()     , name="daily-intake-list"),
    path("api/intake/add/"                  , views.add_to_daily_intake         , name="add-to-daily-intake"),
    path("api/intake/delete/"               , views.delete_from_daily_intake    , name="delete-from-daily-intake"),
    
    #Weight Tracking paths
    path("api/weight/"                      , WeightLogListView.as_view()       , name="weight-list"),
    path("api/weight/record/"               , views.record_weight               , name="record-weight"),
    path("api/weight/update/<int:pk>/"      , views.update_weight               , name="update-weight"),
    path("api/weight/delete/"               , views.delete_weight               , name="delete-weight"),
    
    #Dashboard path
    path("api/dashboard/"                   , DashboardView.as_view()           , name="dashboard")
]

#Media serving in Dev
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
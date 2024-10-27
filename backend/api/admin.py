from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Food, DailyIntake, WeightTracker

# Register your models here.
# list_display for each model displays the fields in the list view of Django Admin Interface
# search_fields add a search bar to the Django Admin Interface, allowing the search of certain fields

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

# Register the Food model
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'calories', 'carbohydrates', 'protein', 'fat')
    search_fields = ('name',)

# Register the DailyIntake model
@admin.register(DailyIntake)
class DailyIntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_eaten', 'food_entry_date')
    search_fields = ('user__username', 'food_eaten__name')
    list_filter = ('food_entry_date',)  # Filters by the date of food entries

# Register the WeightTracker model
@admin.register(WeightTracker)
class WeightTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'weight_entry_date')
    search_fields = ('user__username',)
    list_filter = ('weight_entry_date',)  # Filters by the date of weight entries
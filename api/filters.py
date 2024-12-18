import django_filters
from .models import Food, DailyIntake, WeightTracker

class FoodFilter(django_filters.FilterSet):
    #Partial-match for food name (Ap will get Grape, Apple, etc)
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    
    #Exact-match for food calories (Cal = 200)
    calories = django_filters.NumberFilter(field_name="calories")
    
    #Range-match for food calories (Filter for foods between min and max calories)
    calories_min = django_filters.NumberFilter(field_name="calories", lookup_expr="gte")
    calories_max = django_filters.NumberFilter(field_name="calories", lookup_expr="lte")
    
    #Range-match for protein (Filter for foods between min and max grams of protein)
    protein_min = django_filters.NumberFilter(field_name="protein", lookup_expr="gte")
    protein_max = django_filters.NumberFilter(field_name="protein", lookup_expr="lte")

    #Range-match for fat (Filter for foods between min and max grams of fat)
    fat_min = django_filters.NumberFilter(field_name="fat", lookup_expr="gte")
    fat_max = django_filters.NumberFilter(field_name="fat", lookup_expr="lte")

    #Range-match for carbohydrates (Filter for foods between min and max grams of carbs)
    carbs_min = django_filters.NumberFilter(field_name="carbohydrates", lookup_expr="gte")
    carbs_max = django_filters.NumberFilter(field_name="carbohydrates", lookup_expr="lte")

    class Meta:
        model = Food
        fields = ["name", "calories", "calories_min", "calories_max", "protein_min", "protein_max", "fat_min", "fat_max", "carbs_min", "carbs_max"]
        
class DailyIntakeFilter(django_filters.FilterSet):
    #Date-Range match to filter food entries between specific dates
    date_min = django_filters.DateFilter(field_name="food_entry_date", lookup_expr="gte")
    date_max = django_filters.DateFilter(field_name="food_entry_date", lookup_expr="lte")
    
    #Range-match to filter foods eaten between a certain range of calories
    calories_min = django_filters.NumberFilter(field_name="food_eaten__calories", lookup_expr="gte")
    calories_max = django_filters.NumberFilter(field_name="food_eaten__calories", lookup_expr="lte")
    
    #Partial-match to filter foods by name
    food_name = django_filters.CharFilter(field_name="food_eaten__name", lookup_expr="icontains")
    
    #Add Range-match for specific macronutrients?
    class Meta:
        model = DailyIntake
        fields = ["date_min", "date_max", "calories_min", "calories_max", "food_name"]
    
class WeightLogFilter(django_filters.FilterSet):
    #Date-Range match to filter weight entries between specific dates
    date_min = django_filters.DateFilter(field_name="weight_entry_date", lookup_expr="gte")
    date_max = django_filters.DateFilter(field_name="weight_entry_date", lookup_expr="lte")
    
    #Range-match to filter weight entries between a certain range of weights
    weight_min = django_filters.NumberFilter(field_name="weight", lookup_expr="gte")
    weight_max = django_filters.NumberFilter(field_name="weight", lookup_expr="lte")
    
    class Meta:
        model = WeightTracker
        fields = ["date_min", "date_max", "weight_min", "weight_max"]
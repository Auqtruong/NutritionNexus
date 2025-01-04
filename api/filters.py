import django_filters
from django.core.exceptions import ValidationError
from .models import Food, DailyIntake, WeightTracker

class DynamicFilterSet(django_filters.FilterSet):
    #Base filterset that dynamically applies filters based on the query parameters passed to backend
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        if request and request.GET:
            parsed_filters = self.parse_query_string(request.GET.urlencode())
            if data:
                data = {**data, **parsed_filters}
            else:
                data = parsed_filters
        super().__init__(data, queryset=queryset, request=request, prefix=prefix)
    @staticmethod
    def parse_query_string(query_string):
        """
        Parse query string into dictionary of field: {operator, value}
        Example Input: "food_name:chicken,calories>100"
        Example Output: {
            "food_name": "chicken",
            "calories__gt: 100
        }
        """
        filters = {}
        for filter in query_string.split(","):
            if ":" in filter:
                field, value = filter.split(":", 1)
                filters[field] = value
            elif ">=" in filter:
                field, value = filter.split(">=", 1)
                filters[f"{field}__gte"] = value
            elif "<=" in filter:
                field, value = filter.split("<=", 1)
                filters[f"{field}__lte"] = value
            elif ">" in filter:
                field, value = filter.split(">", 1)
                filters[f"{field}__gt"] = value
            elif "<" in filter:
                field, value = filter.split("<", 1)
                filters[f"{field}__lt"] = value
            elif "=" in filter:
                field, value = filter.split("=", 1)
                filters[field] = value
            else:
                raise ValidationError(f"Invalid filter: {filter}")
        return filters

class FoodFilter(DynamicFilterSet):
    class Meta:
        model = Food
        fields = {
            "name": ["icontains"],
            "calories": ["exact", "gte", "lte"],
            "protein": ["gte", "lte"],
            "carbohydrates": ["gte", "lte"],
            "fat": ["gte", "lte"],
        }
        
class DailyIntakeFilter(DynamicFilterSet):
    class Meta:
        model = DailyIntake
        fields = {
            "food_eaten__name": ["icontains"],
            "food_eaten__calories": ["gte", "lte"],
            "food_entry_date": ["exact", "gte", "lte"],
        }
        
class WeightLogFilter(DynamicFilterSet):
    class Meta:
        model = WeightTracker
        fields = {
            "weight": ["exact", "gte", "lte"],
            "weight_entry_date": ["exact", "gte", "lte"]
        }
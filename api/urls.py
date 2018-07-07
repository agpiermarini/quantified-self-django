from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FoodsView, MealsView, MealFoodsView

urlpatterns = [
    path('api/v1/foods', FoodsView.as_view({'get': 'index', 'post': 'create'})),
    path('api/v1/foods/<food_id>', FoodsView.as_view({'get': 'show', 'patch': 'update', 'put': 'update', 'delete': 'destroy'})),
    path('api/v1/meals', MealsView.as_view({'get': 'index'})),
    path('api/v1/meals/<meal_id>/foods', MealsView.as_view({'get': 'show'})),
    path('api/v1/meals/<meal_id>/foods/<food_id>', MealFoodsView.as_view({'post': 'create', 'delete': 'destroy'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)

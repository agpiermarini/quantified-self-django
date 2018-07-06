from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FoodsView, MealsView

urlpatterns = {
    url(r'^api/v1/foods', FoodsView.as_view({'get': 'index', 'post': 'create'})),
    url(r'^api/v1/foods/(?P<food_id>\d+)', FoodsView.as_view({'get': 'show', 'patch': 'update', 'put': 'update', 'delete': 'destroy'})),
    url(r'^api/v1/meals', MealsView.as_view({'get': 'index'})),
    url(r'^api/v1/meals/(?P<meal_id>\d+)/foods', MealsView.as_view({'get': 'show'})),

}

urlpatterns = format_suffix_patterns(urlpatterns)

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FoodsView

urlpatterns = {
    url(r'^api/v1/foods$', FoodsView.as_view({'get': 'index', 'post': 'create'})),
    url(r'^api/v1/foods/(?P<food_id>\d+)', FoodsView.as_view({'get': 'show', 'patch': 'update', 'put': 'update'}))
}

urlpatterns = format_suffix_patterns(urlpatterns)

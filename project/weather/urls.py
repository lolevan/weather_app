from django.urls import path
from .views import get_weather, search_statistics

app_name = 'weather'

urlpatterns = [
    path('', get_weather, name='get_weather'),
    path('statistics/', search_statistics, name='search_statistics'),
]

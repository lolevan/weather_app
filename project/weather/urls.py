from django.urls import path
from .views import get_weather, search_statistics, get_history, get_last_city


urlpatterns = [
    path('', get_weather, name='get_weather'),
    path('statistics/', search_statistics, name='search_statistics'),
    path('history/', get_history, name='get_history'),
    path('last_city/', get_last_city, name='get_last_city'),
]

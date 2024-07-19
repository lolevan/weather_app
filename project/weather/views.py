import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import WeatherQuery


def get_weather(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        if city:
            # Запрос к API геокодирования для получения координат города
            geo_response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}')
            geo_data = geo_response.json()

            if 'results' in geo_data and geo_data['results']:
                latitude = geo_data['results'][0]['latitude']
                longitude = geo_data['results'][0]['longitude']

                # Запрос к API прогноза погоды с использованием полученных координат
                weather_response = requests.get(
                    f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m')
                weather_data = weather_response.json()

                # Фильтрация данных только на сегодняшнюю дату
                current_date = timezone.now().strftime('%Y-%m-%d')
                hourly_data = list(zip(weather_data['hourly']['time'], weather_data['hourly']['temperature_2m']))
                today_data = [(time.split('T')[1], temp) for time, temp in hourly_data if time.startswith(current_date)]

                weather_query, created = WeatherQuery.objects.get_or_create(city=city)
                if not created:
                    weather_query.query_count += 1
                    weather_query.save()

                return render(request, 'weather/weather.html', {
                    'weather_data': today_data,
                    'city': city,
                    'current_date': current_date,
                })
            else:
                error_message = 'Город не найден'
                return render(request, 'weather/weather.html', {'error_message': error_message})

    return render(request, 'weather/weather.html')


def search_statistics(request):
    statistics = WeatherQuery.objects.all().values('city', 'query_count')
    return JsonResponse(list(statistics), safe=False)

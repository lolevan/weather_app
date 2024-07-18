import requests
from django.shortcuts import render


def get_weather(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        if city:
            # Запрос к API геокодирования для получения координат города
            geo_response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}')
            geo_data = geo_response.json()

            if geo_data['results']:
                latitude = geo_data['results'][0]['latitude']
                longitude = geo_data['results'][0]['longitude']

                # Запрос к API прогноза погоды с использованием полученных координат
                weather_response = requests.get(
                    f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m')
                weather_data = weather_response.json()

                return render(request, 'weather/weather.html', {'weather_data': weather_data})

    return render(request, 'weather/weather.html')



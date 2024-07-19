from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone

from .models import WeatherQuery

import requests


def get_weather(request):
    show_last_city_modal = False
    last_city = None

    # Проверка, если в сессии есть последний просмотренный город и параметр 'city' не передан
    if 'last_city' in request.session and not request.GET.get('city'):
        show_last_city_modal = True
        last_city = request.session['last_city']

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

                # Обновление или создание записи в базе данных для данного города
                weather_query, created = WeatherQuery.objects.get_or_create(city=city)
                if not created:
                    weather_query.query_count += 1
                    weather_query.save()

                # Сохранение истории поиска в сессии
                if 'search_history' not in request.session:
                    request.session['search_history'] = []
                if city not in request.session['search_history']:
                    request.session['search_history'].append(city)
                request.session['last_city'] = city

                # Рендеринг страницы с данными о погоде
                return render(request, 'weather/weather.html', {
                    'weather_data': today_data,
                    'city': city,
                    'current_date': current_date,
                    'show_last_city_modal': show_last_city_modal,
                    'last_city': last_city,
                })
            else:
                # Если город не найден, отображаем сообщение об ошибке
                error_message = 'City not found.'
                return render(request, 'weather/weather.html', {
                    'error_message': error_message,
                    'show_last_city_modal': show_last_city_modal,
                    'last_city': last_city,
                })

    # Если метод запроса не GET, просто рендерим страницу без данных о погоде
    return render(request, 'weather/weather.html', {
        'show_last_city_modal': show_last_city_modal,
        'last_city': last_city,
    })


def search_statistics(request):
    # Получение статистики запросов по городам
    statistics = WeatherQuery.objects.all().values('city', 'query_count')
    return JsonResponse(list(statistics), safe=False)


def get_history(request):
    # Получение истории поиска из сессии
    history = request.session.get('search_history', [])
    return JsonResponse({'history': history})


def get_last_city(request):
    # Получение последнего просмотренного города из сессии
    last_city = request.session.get('last_city', None)
    return JsonResponse({'last_city': last_city})

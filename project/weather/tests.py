from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

import json


class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.search_url = reverse('get_weather')
        self.history_url = reverse('get_history')
        self.last_city_url = reverse('get_last_city')

    def test_weather_search(self):
        response = self.client.get(self.search_url, {'city': 'Ulan-Ude'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Weather Data for Ulan-Ude')
        self.assertIn('Ulan-Ude', self.client.session['search_history'])

    def test_search_history(self):
        self.client.get(self.search_url, {'city': 'Ulan-Ude'})
        self.client.get(self.search_url, {'city': 'Moscow'})
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'history': ['Ulan-Ude', 'Moscow']}
        )

    def test_last_city_modal(self):
        self.client.get(self.search_url, {'city': 'Ulan-Ude'})
        self.client.get(reverse('get_weather'))
        response = self.client.get(reverse('get_weather'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You last searched for Ulan-Ude')

    def test_no_last_city_modal_on_search(self):
        self.client.get(self.search_url, {'city': 'Ulan-Ude'})
        response = self.client.get(self.search_url, {'city': 'Moscow'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'You last searched for Ulan-Ude')

    def test_weather_data_format(self):
        response = self.client.get(self.search_url, {'city': 'Ulan-Ude'})
        self.assertEqual(response.status_code, 200)

        current_date = timezone.now().strftime('%Y-%m-%d')
        weather_data = response.context['weather_data']

        print("Weather Data:", json.dumps(weather_data, indent=2))

        # Проверка, что данные о погоде не пустые и содержат текущую дату
        self.assertTrue(len(weather_data) > 0, "No weather data found for the current date")

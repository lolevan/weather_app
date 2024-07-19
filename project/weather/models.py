from django.db import models


class WeatherQuery(models.Model):
    city = models.CharField(max_length=100)
    query_count = models.IntegerField(default=1)
    last_queried = models.DateTimeField(auto_now=True)

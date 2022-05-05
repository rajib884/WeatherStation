from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='sensors', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    class AirDirection(models.TextChoices):
        NORTH = 'N'
        NORTH_EAST = 'NE'
        EAST = 'E'
        SOUTH_EAST = 'SE'
        SOUTH = 'S'
        SOUTH_WEST = 'SW'
        WEST = 'W'
        NORTH_WEST = 'NW'

    date = models.DateTimeField("Date Collected", primary_key=True)
    temperature = models.FloatField("Temperature")
    humidity = models.IntegerField("Humidity")
    pressure = models.IntegerField("Pressure")
    air_speed = models.FloatField("Air Speed")
    air_direction = models.CharField(
        max_length=2,
        choices=AirDirection.choices,
    )
    sensor = models.ForeignKey(Sensor, related_name='datapoint', on_delete=models.CASCADE)

    def __str__(self):
        return self.date.astimezone(pytz.timezone("Asia/Dhaka")).strftime("%Y-%m-%d %H:%M:%S GMT%Z")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

from djongo import models
# from djongo.models import forms
from django.contrib.auth.models import User

# Create your models here.
class Rider(models.Model):
    current_location = models.CharField(max_length = 50)
    destination = models.CharField(max_length = 50)
    total_trips = models.IntegerField()
    rating = models.IntegerField()
    no_show = models.IntegerField()
    user_key = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Driver(models.Model):
    current_location = models.CharField(max_length = 50)
    pickup_distance = models.IntegerField()
    trip_distance = models.IntegerField()
    rate = models.IntegerField()
    rush_hour_rate = models.IntegerField()
    vehicle_type = models.CharField(max_length = 250)
    vehicle_make = models.CharField(max_length = 250)
    vehicle_model = models.CharField(max_length = 250)
    vehicle_year = models.IntegerField()
    vehicle_insured = models.BooleanField()
    license_expiration = models.DateField()
    total_trips = models.IntegerField()
    safety_rating = models.IntegerField()
    time_rating = models.IntegerField()
    service_rating = models.IntegerField()
    no_show = models.IntegerField()
    user_key = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    comment = models.TextField(max_length = 500)
    driver_key = models.ForeignKey(User, on_delete = models.CASCADE)
    rider_key = models.ForeignKey(User, on_delete = models.CASCADE)
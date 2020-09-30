from djongo import models
# from djongo.models import forms
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.
class Rider(models.Model):
    current_location = models.CharField(max_length = 50, default = "N/A")
    destination = models.CharField(max_length = 50, default = "N/A")
    total_trips = models.IntegerField(default = 0)
    rating = models.IntegerField(default = None)
    no_show = models.IntegerField(default = 0)
    user_key = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Driver(models.Model):
    current_location = models.CharField(max_length = 50, default = "N/A")
    pickup_distance = models.IntegerField(default = 1)
    trip_distance = models.IntegerField(default = 0)
    rate = models.IntegerField(default = 1)
    rush_hour_rate = models.IntegerField(default = 1)
    vehicle_type = models.CharField(max_length = 250, default = "N/A")
    vehicle_make = models.CharField(max_length = 250, default = "N/A")
    vehicle_model = models.CharField(max_length = 250, default = "N/A")
    vehicle_year = models.IntegerField(default = 0)
    vehicle_insured = models.BooleanField(default = False)
    license_expiration = models.DateField(default = date(2000, 1, 1))
    total_trips = models.IntegerField(default = 0)
    safety_rating = models.IntegerField(default = None)
    time_rating = models.IntegerField(default = None)
    service_rating = models.IntegerField(default = None)
    no_show = models.IntegerField(default = 0)
    user_key = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return "/profile/{}/d".format(User.objects.get(pk = self.user_key))

class Review(models.Model):
    comment = models.TextField(max_length = 500)
    driver_key = models.IntegerField()
    rider_key = models.ForeignKey(User, on_delete = models.CASCADE)
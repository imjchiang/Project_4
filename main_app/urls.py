from django.urls import path
from . import views

# set paths for pages here
urlpatterns = [
    path("", views.index, name = "index"),
    path("profile/r/", views.rider_profile, name = "rider_profile"),
    path("profile/d/", views.driver_profile, name = "driver_profile"),
]
from django.urls import path
from . import views

# set paths for pages here
urlpatterns = [
    path("", views.index, name = "index"),
    path("profile/<username>/", views.profile, name = "profile"),
    path("profile/<username>/r/", views.rider_profile, name = "rider_profile"),
    path("profile/<username>/d/", views.driver_profile, name = "driver_profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("rider/create/", views.RiderCreate.as_view(), name="rider_create"),
    path("driver/create/", views.DriverCreate.as_view(), name="driver_create"),
    path("driver/update/<int:pk>", views.DriverUpdate.as_view(), name="driver_update"),
    path("ride/create/", views.RideCreate.as_view(), name="ride_create"),
]
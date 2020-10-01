from django import forms

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from .models import Rider, Driver, Ride


####################### FORMS #######################
class MyUserCreationForm(UserCreationForm):
    # set email to be a required part of the form
    email = forms.EmailField(required=True, label='Email')

    # form creation with fields to be used
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    # what to save in the form
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])

        # ensures no duplicate emails (username no duplicate is already included as default)
        if User.objects.filter(email=user.email).exists():
            raise ValidationError("Email has already been used. Please use a different one.")
        
        if commit:
            user.save()
        return user

####################### USER #######################

def login_view(request):
    if request.method == "POST":
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user) # login user by creating a session
                    return HttpResponseRedirect("/profile/" + u)
                else:
                    raise ValidationError("The account has been disabled.")
            else:
                raise ValidationError("The username and/or password is incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def signup_view(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/profile/" + str(user))
        else:
            return HttpResponse("<h1>Try Again</h1>")
    else:
        form = MyUserCreationForm()
        return render(request, "signup.html", {"form": form})

@login_required
def profile(request, username):
    profile_user = User.objects.get(username = username)
    user = User.objects.get(pk = request.user.id)

    # if someone is accessing their own profile
    if user.username == username:
        personal_profile = True
    else:
        personal_profile = False
    # if Rider for the user exists, pass parameter to rider profile redirect
    if Rider.objects.filter(user_key_id = user.id).exists():
        rider_register = True
    # otherwise profile page redirect to rider form
    else: 
        rider_register = False
    
    # if Driver for the user exists, pass parameter to driver profile redirect
    if Driver.objects.filter(user_key_id = user.id).exists():
        driver_register = True
    # otherwise profile page redirect to driver form
    else: 
        driver_register = False
    return render(request, "profile.html", {"profile_user": profile_user, "rider_register": rider_register, "driver_register": driver_register, "personal_profile": personal_profile})


####################### RIDER #######################

# profile page for riders
@login_required
def rider_profile(request, username):
    profile_user = User.objects.get(username = username)
    rider_prof = Rider.objects.get(user_key = profile_user.id)
    user = User.objects.get(pk = request.user.id)

    # if someone is accessing their own profile
    if user.username == username:
        personal_profile = True
    else:
        personal_profile = False

    return render(request, "riders/profile.html", {"profile_user": profile_user, "rider_prof": rider_prof, "personal_profile": personal_profile})

# create a new rider
class RiderCreate(CreateView):
    model = Rider
    fields = []

    def form_valid(self, form):
        # get User object of the logged in account
        user = User.objects.get(pk = self.request.user.id)
        rider = form.save(commit = False)
        # set user_key to the user object grabbed
        rider.user_key = user

        # ensures there are no riders associated with the account
        if Rider.objects.filter(user_key_id = user.id).exists():
            # don't register rider if there is already one registered
            raise ValidationError("You cannot create another Rider in your account.")
        # register a new rider and redirect to profile page of rider
        else:
            rider.save()
            return HttpResponseRedirect("/profile/{}/r".format(self.request.user.username))
            # [possible alternative] return super(RiderCreate, self).form_valid(form)
        

####################### DRIVER #######################

# profile page for drivers
@login_required
def driver_profile(request, username):
    profile_user = User.objects.get(username = username)
    driver_prof = Driver.objects.get(user_key = profile_user.id)
    user = User.objects.get(pk = request.user.id)

    # if someone is accessing their own profile
    if user.username == username:
        personal_profile = True
    else:
        personal_profile = False
        
    return render(request, "drivers/profile.html", {"profile_user": profile_user, "driver_prof": driver_prof, "personal_profile": personal_profile})

# create a new rider
class DriverCreate(CreateView):
    model = Driver
    fields = ["trip_distance", "rate", "rush_hour_rate", "vehicle_type", "vehicle_make", "vehicle_model", "vehicle_year", "vehicle_insured", "license_expiration"]

    def get_form(self, form_class = None):
        form = super(DriverCreate, self).get_form(form_class)
        form.fields["trip_distance"].required = True
        form.fields["rate"].required = True
        form.fields["rush_hour_rate"].required = True
        form.fields["vehicle_type"].required = True
        form.fields["vehicle_make"].required = True
        form.fields["vehicle_model"].required = True
        form.fields["vehicle_year"].required = True
        form.fields["license_expiration"].required = True
        
        return form

    def form_valid(self, form):
        # get User object of the logged in account
        user = User.objects.get(pk = self.request.user.id)
        driver = form.save(commit = False)
        # set user_key to the user object grabbed
        driver.user_key = user

        # ensures there are no drivers associated with the account
        if Driver.objects.filter(user_key_id = user.id).exists():
            # don't register driver if there is already one registered
            raise ValidationError("You cannot create another Driver in your account.")
        # register a new driver and redirect to profile page of rider
        else:
            driver.save()
            return HttpResponseRedirect("/profile/{}/d".format(self.request.user.username))

class DriverUpdate(UpdateView):
    model = Driver
    fields = ["trip_distance", "rate", "rush_hour_rate", "vehicle_type", "vehicle_make", "vehicle_model", "vehicle_year", "vehicle_insured", "license_expiration"]
    
    def form_valid(self, form):
        if self.request.user.id:
            # get User object of the logged in account
            user = User.objects.get(pk = self.request.user.id)
            driver = form.save(commit=False)
            if user.id == driver.pk:
                driver.save()
                return HttpResponseRedirect("/profile/{}/d".format(self.request.user.username))
            raise ValidationError("You cannot update a different User's driver account.")
        else:
            raise ValidationError("You cannot update a different User's driver account.")

####################### RIDE #######################

def show_ride(request, pk):
    ride = Ride.objects.get(pk = pk)
    rider = User.objects.get(pk = ride.rider_key.pk)

    if request.user:
        signed_in_user = request.user
    else:
        signed_in_user = None


    if ride.driver_key == None:
        driver = None
    else:
        driver = User.objects.get(pk = ride.driver_key)

    if ride.rider_key.pk == request.user.id:
        ride_update = True
    else:
        ride_update = False

    return render(request, "show_ride.html", {"ride": ride, "ride_update": ride_update, "rider": rider, "driver": driver, "signed_in_user": signed_in_user})

@login_required
def driver_ride(request, pk):
    ride = Ride.objects.get(pk = pk)

    if ride.driver_key == None:
        Ride.objects.filter(pk = pk).update(driver_key = request.user.id)
        return HttpResponseRedirect("/ride/{}".format(pk))
    else:
        raise ValidationError("There is already a driver for this ride.")

class RideCreate(CreateView):
    model = Ride
    fields = ["start_location", "destination"]

    def form_valid(self, form):
        # get User object of the logged in account
        user = User.objects.get(pk = self.request.user.id)
        ride = form.save(commit = False)
        if (user and user.id):
            ride.rider_key = user
            ride.save()
            return HttpResponseRedirect("/ride/{}".format(ride.pk))
        raise ValidationError("Must be logged in to request a ride.")

class RideUpdate(UpdateView):
    model = Ride
    fields = ["start_location", "destination"]

    def form_valid(self, form):
        # get User object of the logged in account
        user = User.objects.get(pk = self.request.user.id)
        ride = form.save(commit = False)
        if (user and user.id == ride.rider_key):
            ride.save()
            return HttpResponseRedirect("/ride/{}".format(ride.pk))
        raise ValidationError("Must be logged in to the right account to update your ride.")


####################### DEFAULT #######################

# home page
def index(request):
    return render(request, "index.html")

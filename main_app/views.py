from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


####################### RIDER #######################

# profile page for riders
def rider_profile(request):
    return render(request, "riders/profile.html")

####################### DRIVER #######################

# profile page for drivers
def driver_profile(request):
    return render(request, "drivers/profile.html")

####################### DEFAULT #######################

# home page
def index(request):
    return render(request, "index.html")

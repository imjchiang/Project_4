from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


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
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/profile/" + str(user))
        else:
            return HttpResponse("<h1>Try Again</h1>")
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})

@login_required
def profile(request, username):
    return render(request, "profile.html", {"username": username})


####################### RIDER #######################

# profile page for riders
@login_required
def rider_profile(request, username):
    return render(request, "riders/profile.html", {"username": username})

####################### DRIVER #######################

# profile page for drivers
@login_required
def driver_profile(request, username):
    return render(request, "drivers/profile.html", {"username": username})

####################### DEFAULT #######################

# home page
def index(request):
    return render(request, "index.html")

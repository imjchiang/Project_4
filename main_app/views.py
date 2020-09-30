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

from .models import Rider, Driver


####################### FORMS #######################
class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if User.objects.filter(email=user.email).exists():
            raise ValidationError("Email has already been used. Please use a different one.")
        
        if commit:
            user.save()
        return user

class RiderForm(forms.Form):
    class Meta:
        model: Rider
        fields = ["current_location", "destination", "user_key"]
    

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
    # if Rider for the user exists, pass rider info.
    # otherwise send rider form to profile page
    # same thing for driver
    return render(request, "profile.html", {"username": username})


####################### RIDER #######################

# profile page for riders
@login_required
def rider_profile(request, username):
    return render(request, "riders/profile.html", {"username": username})

class RiderCreate(CreateView):
    model = Rider
    fields = []

    def form_valid(self, form):
        user = User.objects.get(pk = self.request.user.id)
        rider = form.save(commit = False)
        rider.user_key = user
        if Rider.objects.filter(user_key_id = user.id).exists():
            raise ValidationError("You cannot create another Rider in your account.")
        else:
            rider.save()
            return HttpResponseRedirect("/profile/{}/r".format(self.request.user.username))
            # return super(RiderCreate, self).form_valid(form)
        

####################### DRIVER #######################

# profile page for drivers
@login_required
def driver_profile(request, username):
    return render(request, "drivers/profile.html", {"username": username})

####################### DEFAULT #######################

# home page
def index(request):
    return render(request, "index.html")

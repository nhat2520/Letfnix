from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import RegisterForm


# Create your views here.
def helloworld(request):
    return render(request, 'helloworld.html', {})


def home(request):
    return render(request, 'home.html', {})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            messages.success(request, "You have been logged in...")
            return redirect('home')
        else:
            messages.success(request, "There was an error, ...")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username,
                                password=password)
            login(request, user)
            messages.success(request, "You have registered successfully")
            return redirect('home')
        else:
            messages.success(request, "There have been a problem")
            return redirect('register')
    else:
        return render(request, 'register.html', {"form": form})

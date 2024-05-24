from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
import random

from .models import (  # noqa
    Movie,
    Profile,
    Category,
    MovieCategory,
    Movie
)
from .forms import (
    RegisterForm,
    UpdateUserForm,
    ChangePasswordForm,
    UserInfoForm
)


# Create your views here.
def helloworld(request):
    return render(request, 'app/movie.html', {})


def home(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        movies = Movie.objects.all()
        random_movie = random.choice(movies)
        print(random_movie)
        recent_movies = Movie.objects.order_by('vote_average')[:6]
        print(recent_movies)
        return render(request, 'app/home.html',
                      {"random_movie": random_movie,
                       "recent_movies": recent_movies,
                       "categories": categories})
    else:
        return redirect('login')


def movie(request, pk):
    movie = Movie.objects.get(movie_id=pk)
    recent_movies = Movie.objects.order_by('vote_average')[:6]
    return render(request, "app/movie.html", {"movie": movie,
                                              "recent_movies": recent_movies})


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
        return render(request, 'auth/login.html', {})


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
        return render(request, 'auth/register.html', {"form": form})


def search_by_name(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        print(searched)
        movies = Movie.objects.filter(Q(name__icontains=searched))

        if not searched:
            print()
            messages.success(request,
                             "Movie doesn't exist")
            return render(request, "app/search.html", {})
        else:
            return render(request, "app/search.html", {"movies": movies,
                                                       "searched": searched})

    else:
        return render(request, "app/search.html", {})


def update_password(request):
    if request.user.is_authenticated:
        curr_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(curr_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Your password has benn updated")
                login(request, curr_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(curr_user)
            return render(request, "update_password.html",
                          {"form": form})
    else:
        messages.success(request, "You must be logged in to do this")
        return redirect('login')


def profile_user(request):
    if request.user.is_authenticated:
        curr_user = request.user
        profile = Profile.objects.filter(user=curr_user)
        return render(request, "profile.html", {"profile": profile})
    else:
        messages.success(request, "You must be logged in to do this")
        return redirect('login')


def update_info(request):
    if request.user.is_authenticated:
        curr_user = Profile.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=curr_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Info has been updated")
            return redirect("profile")
        return render(request, "update_info.html", {"form": form})

    else:
        return render(request, "search.html", {})


def update_user(request):
    if request.user.is_authenticated:
        curr_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,
                                   instance=curr_user)

        if user_form.is_valid():
            user_form.save()

            login(request, curr_user)
            messages.success(request, "User has been updated")
            return redirect("home")
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, "You don't have permission to do this")
        return redirect("login")


def category(request, cat):
    try:
        movies = Movie.objects.filter(moviecategory__category__name=cat)
        print(1)
        return render(request, 'app/category.html', {"movies": movies,
                                                     "cat": cat})

    except:  # noqa
        print("error")
        messages.success(request, ("That category doesn't exist"))
        return redirect('home')


def category_all(request):
    categories = Category.objects.all()
    return render(request, "navbar.html", {"categories": categories})

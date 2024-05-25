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
    Movie,
    Library
)
from .forms import (
    RegisterForm,
    UpdateUserForm,
    ChangePasswordForm,
    UserInfoForm
)
from recommend import (
    create_and_save_tfidf_matrix_v1,
    create_and_save_user_profile,
    calculate_and_save_similarity_matrix,
    get_recommendations,
)


# Create your views here.
def helloworld(request):
    return render(request, 'app/movie.html', {})


def home(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        movies = Movie.objects.all()
        user = request.user
        recommend_movie = get_recommendations(user.id, 7)

        print(recommend_movie["title"])
        rec_mov = []
        for movie in recommend_movie["title"]:
            rec_mov.append(Movie.objects.get(name=movie))
        print(rec_mov)
        random_movie = random.choice(movies)

        recent_movies = Movie.objects.order_by('-vote_average')[6:12]
        print(random_movie)
        recent_movies = Movie.objects.order_by('-vote_average')[:6]
        print(recent_movies)
        return render(request, 'app/home.html',
                      {"random_movie": random_movie,
                       "recent_movies": recent_movies,
                       "rec_mov": rec_mov,
                       "categories": categories})
    else:
        return redirect('login')


def movie(request, pk):
    movie = Movie.objects.get(movie_id=pk)
    genres = MovieCategory.objects.filter(movie_id=pk)
    categories = []
    for genre in genres:
        category = Category.objects.get(category_id=genre.category_id)
        categories.append(category)
    recent_movies = Movie.objects.order_by('-vote_average')[6:12]
    return render(request, "app/movie.html", {"movie": movie,
                                              "recent_movies": recent_movies,
                                              "categories": categories})


def login_view(request):
    create_and_save_tfidf_matrix_v1()
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

            create_and_save_user_profile(user.id, "v1")
            calculate_and_save_similarity_matrix(user.id, "v1")
            return redirect('home')
        else:
            messages.success(request, "There have been a problem")
            return render(request, 'auth/register.html', {"form": form})
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
                return redirect('profile')
            else:
                print(form.errors)
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            
            return render(request, "user/update_password.html",
                          {"user": curr_user})
    else:
        messages.success(request, "You must be logged in to do this")
        return redirect('login')


def profile_user(request):
    if request.user.is_authenticated:
        curr_user = request.user
        profile = Profile.objects.get(user__id=request.user.id)
        return render(request, "user/profile.html", {"profile": profile, "user": curr_user})
    else:
        messages.success(request, "You must be logged in to do this")
        return redirect('login')

def view_library(request):
    if request.user.is_authenticated:
        curr_user = request.user
        libraries = Library.objects.filter(user=curr_user)
        movies = []
        for library in libraries:
            movies.append(Movie.objects.get(movie_id=library.movie_id))
        return render(request, "user/my_movie.html", {"user": curr_user, "movies":movies})
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

        user_form = UpdateUserForm()
        profile_form = UserInfoForm()
        if request.method == "POST":
            curr_user = User.objects.get(id=request.user.id)
            curr_profile = Profile.objects.get(user__id=request.user.id)

            user_form = UpdateUserForm(request.POST or None,
                                       instance=curr_user)
            profile_form = UserInfoForm(request.POST or None,
                                        instance=curr_profile)
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
            print(user_form.errors)
            print(profile_form.errors)  
            return redirect('profile')
        else:
            return render(request, "user/update_user.html", {"user_form": user_form,
                                                        "profile_form": profile_form})


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

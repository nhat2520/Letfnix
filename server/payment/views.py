from django.shortcuts import render, redirect
from django.contrib import messages

from app.models import Profile, Movie, Library

from cart.models import CartItem  # noqa

from .forms import AddFundsForm
from decimal import Decimal

# Create your views here.
def payment_success(request):
    return render(request, 'user/payment_success.html', {})

def billing_info(request):
    if request.user.is_authenticated:
        curr_user = request.user
        profile = Profile.objects.get(user__id=request.user.id)
        print(profile.balance)
        movies = Movie.objects.filter(cartitem__user=curr_user)
        total_price = sum(movie.price for movie in movies) 
        return render(request, "user/bill.html", {"movies": movies,
                                             "total_price": total_price,
                                             "profile": profile})
    else:
        messages.success(request, "You don't have permission to do that")
        return redirect("login")


def add_funds(request):
    if request.user.is_authenticated:
        curr_user = request.user
        profile = Profile.objects.get(user=curr_user)
        form = AddFundsForm()
        if request.method == "POST":
            form = AddFundsForm(request.POST)
            if form.is_valid():
                money = form.cleaned_data["amount"]
                profile.balance = profile.balance + money
                profile.save()
                return redirect('home')
            else:
                print("Something went wrong")
                messages.success("Something went wrong")
                return redirect('add_funds')
        else:
            print("error")
            return render(request, 'user/add_funds.html', {"form": form})
    else:
        messages.success(request, ("You have no permission to do that"))
        return redirect('login')


def processing(request):
    curr_user = request.user
    total_price = Decimal(request.POST['total_price'])
    profile = Profile.objects.get(user=curr_user)
    if profile.balance >= total_price:
        profile.balance = profile.balance - total_price
        profile.save()
        movies = Movie.objects.filter(cartitem__user=curr_user)
        for movie in movies:
            Library.objects.create(user=curr_user, movie=movie)
        CartItem.objects.filter(user=curr_user).delete()
        return redirect('success')
    else:
        messages.success(request, "You don't have enough money, please add funds")  # noqa
        return redirect('add_funds')

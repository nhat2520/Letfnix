from django.shortcuts import render, redirect
from django.contrib import messages

from app.models import Profile, Movie

from cart.models import CartItem  # noqa

from .forms import AddFundsForm


# Create your views here.
def payment_success(request):
    return render(request, 'payment_success.html', {})


def billing_info(request):
    if request.user.is_authenticated:
        curr_user = request.user

        movies = Movie.object.filter(cartitem__user=curr_user)
        total_price = sum(movie.price for movie in movies)

        return render(request, "bill.html", {"movies": movies,
                                             "total_price": total_price})
    else:
        messages.success(request, "You don't have permission to do that")
        return redirect("login")


def add_funds(request):
    if request.user.is_authenticated:
        curr_user = request.user
        profile = Profile.objects.filter(user=curr_user)
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
            messages.success(request, "There was an error, ...")
            return render(request, 'add_funds.html', {"form": form})
    else:
        messages.success(request, ("You have no permission to do that"))
        return redirect('login')


def process(request, total_price):
    curr_user = request.user
    profile = Profile.objects.filter(user=curr_user)
    if profile.balance >= total_price:
        profile.balance = profile.balance - total_price
        profile.save()
        return redirect('payment_success')
    else:
        messages.success(request, "You don't have enough money, please add funds")  # noqa
        return redirect('add_funds')

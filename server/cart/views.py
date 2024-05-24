from django.shortcuts import render, redirect

from app.models import Movie
from .models import CartItem


# Create your views here.
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.movie.price for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items,
                                         "total_price": total_price})


def add_to_cart(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    cart_item, created = CartItem.objects.get_or_create(
        movie=movie,
        user=request.user
    )
    cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, movie_id):
    cart_item = CartItem.objects.get(id=movie_id)
    cart_item.delete()
    return redirect("view_cart")

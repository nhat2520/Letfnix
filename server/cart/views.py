from django.shortcuts import render, redirect
from urllib.parse import parse_qs
from app.models import Movie
from .models import CartItem
import json

# Create your views here.
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.movie.price for item in cart_items)
    return render(request, "app/cart.html", {"cart_items": cart_items,
                                         "total_price": total_price})


def add_to_cart(request):
    body_str = request.body.decode('utf-8')
    parsed_body = parse_qs(body_str)
    movie_id = parsed_body.get('movie_id', [None])[0]
        
    print("Product ID:", movie_id)
    movie = Movie.objects.get(movie_id=movie_id)
    cart_item, created = CartItem.objects.get_or_create(
        movie=movie,
        user=request.user
    )
    cart_item.save()
    return redirect('view_cart')



def remove_from_cart(request):
    body_str = request.body.decode('utf-8')
    parsed_body = parse_qs(body_str)
    movie_id = parsed_body.get('movie_id', [None])[0]
        
    print("Product ID:", movie_id)
    cart_item = CartItem.objects.get(movie_id=movie_id)
    cart_item.delete()
    return redirect("view_cart")

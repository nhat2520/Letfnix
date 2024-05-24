from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name="view_cart"),
    path('add/', views.add_to_cart, name="add"),
    path('delete/', views.remove_from_cart, name="remove"),
]

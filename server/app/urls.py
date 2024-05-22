from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('helloworld', views.helloworld, name="helloworld"),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('movie/<str:pk>', views.movie, name="movie"),
    path('search', views.search_by_name, name="search")
]

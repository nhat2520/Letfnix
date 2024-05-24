from django.urls import path
from . import views
       
urlpatterns = [
    path('', views.home, name='home'),
    path('helloworld', views.helloworld, name="helloworld"),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('movie/<str:pk>', views.movie, name="movie"),
    path('search', views.search_by_name, name="search"),
    path('profile', views.profile_user, name="profile"),
    path('profile/update_user', views.update_user, name="update_user"),
    path('profile/update_password', views.update_password,
         name="update_password"),
    path('profile/update_info', views.update_info, name="update_info"),
    path('category/<str:cat>', views.category, name="category"),
    path("category", views.category_all, name="category_all")
]

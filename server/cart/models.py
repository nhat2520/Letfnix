from django.db import models
from django.contrib.auth.models import User

from app.models import Movie


# Create your models here.
class CartItem(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie.name

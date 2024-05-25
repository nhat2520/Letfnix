from django.db import models
from django.contrib.auth.models import User
from app.models import Movie


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    date_ordered = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order - {str(self.id)}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order - {str(self.id)}"

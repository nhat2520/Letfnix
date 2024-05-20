import uuid
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.utils import timezone


# Create your models here.
class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True,
                                   default=uuid.uuid4(),
                                   editable=False,
                                   unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=50, blank=False)
    phone_number = PhoneNumberField(blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4(),
                                  editable=False,
                                  unique=True)
    payment_method = models.CharField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.payment_id


class Favorite_list(models.Model):
    favorite_list_id = models.UUIDField(primary_key=True,
                                        default=uuid.uuid4(),
                                        editable=False,
                                        unique=True)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 blank=True)

    def __str__(self):
        return self.favorite_list_id


class Category(models.Model):
    category_id = models.UUIDField(primary_key=True,
                                   default=uuid.uuid4(),
                                   editable=False,
                                   unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True,
                                default=uuid.uuid4(),
                                editable=False,
                                unique=True,
                                )
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 blank=True)
    payment = models.ForeignKey(Payment,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4(),
                               editable=False,
                               unique=True)
    quantity = models.IntegerField()
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 default=None)

    def __str__(self):
        return self.cart_id


class Movie(models.Model):
    movie_id = models.UUIDField(primary_key=True,
                                default=uuid.uuid4(),
                                editable=False,
                                unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trailer_url = models.CharField(100)
    vote_average = models.DecimalField(max_digits=2, decimal_places=2)
    image = models.ImageField(upload_to="uploads/movie/")
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 default=1)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              blank=True)
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             blank=True)
    favorite_list = models.OneToOneField(Favorite_list,
                                         on_delete=models.CASCADE)

    def __str__(self):
        return self.name

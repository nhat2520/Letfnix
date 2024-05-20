import uuid
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.utils import timezone

PAYMENT_METHOD_CHOICES = [
        ('PP', 'PayPal'),
        ('ST', 'STRIPE'),
    ]
CATEGORY_CHOICES = [
    ('SF', 'Science Fiction'),
    ('ADV', 'Adventure'),
    ('ACT', 'Action'),
    ('FAN', 'Fantasy'),
    ('COM', 'Comedy'),
    ('DRA', 'Drama'),
    ('THR', 'Thriller'),
    ('CRI', 'Crime'),
    ('WAR', 'War'),
    ('MYS', 'Mystery'),
    ('HOR', 'Horror')
]

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
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    def __str__(self):
        return self.payment_id



class Favorite_list(models.Model):
    favorite_list_id = models.UUIDField(primary_key=True,
                                default=uuid.uuid4(),
                                editable=False,
                                unique=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)    

    def __str__(self):
        return self.favorite_list_id


class Category(models.Model):

    category_id = models.UUIDField(primary_key=True,
                                   default=uuid.uuid4(),
                                   editable=False,
                                   unique=True)
    name = models.CharField(choices=CATEGORY_CHOICES)

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
    poster_path = models.URLField(blank=True)
    backdrop_path = models.URLField(blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              blank=True)
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             blank=True)
    favorite_list = models.ForeignKey(Favorite_list,
                                    on_delete=models.CASCADE,
                                    blank=True)

    def __str__(self):
        return self.name

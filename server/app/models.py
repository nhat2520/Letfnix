import uuid
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

PAYMENT_METHOD_CHOICES = [
        ('PP', 'PayPal'),
        ('ST', 'STRIPE'),
    ]

CATEGORY_CHOICES = [
    ('ACT', 'Action'),
    ('ADV', 'Adventure'),
    ('ANI', 'Animation'),
    ('COM', 'Comedy'),
    ('CRI', 'Crime'),
    ('DOC', 'Documentary'),
    ('DRA', 'Drama'),
    ('FAM', 'Family'),
    ('FAN', 'Fantasy'),
    ('HIS', 'History'),
    ('HOR', 'Horror'),
    ('MUS', 'Music'),
    ('MYS', 'Mystery'),
    ('ROM', 'Romance'),
    ('SF', 'Science Fiction'),
    ('TVM', 'TV Movie'),
    ('THR', 'Thriller'),
    ('WAR', 'War'),
    ('WES', 'Western')
]


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(default="default.jpg",
                               upload_to="media/uploads")
    date_of_birth = models.DateField(blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2,
                                  default=1000.00)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


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
                                   default=uuid.uuid4,
                                   editable=False)
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES,
                            unique=True)

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
                                 null=True,)
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
    customer = models.OneToOneField(Customer,
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
    vote_average = models.DecimalField(max_digits=4, decimal_places=3)
    poster_path = models.URLField(blank=True)
    backdrop_path = models.URLField(blank=True)
    nation = models.CharField(max_length=50, blank=True)
    run_time = models.IntegerField()
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True,)
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             null=True,)
    favorite_list = models.ForeignKey(Favorite_list,
                                      on_delete=models.CASCADE,
                                      null=True,)

    def __str__(self):
        return self.name


class MovieCategory(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'category')

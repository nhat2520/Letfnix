from django.contrib import admin
from .models import (
    Category,
    Cart,
    Customer,
    Favorite_list,
    Movie,
    Order,
    Payment,
)


# class CustomerAdmin(admin.ModelAdmin):
#     list_display = [
#         "firstname",
#         "lastname",
#         "email",
#         "phone_number",
#     ]

#     list_filter = [
#         "firstname",
#         "lastname",
#         "email",
#         "phone_number",
#     ]

#     search_fields = [
#         "email",
#         "phone_number"
#     ]


# class MovieAdmin(admin.ModelAdmin):
#     list_display = [
#         "name",
#         "description",
#         "price",
#         "vote_average"
#     ]

#     list_filter = ["name", "price"]

#     search_fields = ["name"]


# Register your models here.
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Favorite_list)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(Payment)

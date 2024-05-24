from django.contrib import admin
from .models import (
    Category,
    Cart,
    Customer,
    Favorite_list,
    Movie,
    Order,
    Payment,
    Profile
)
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Favorite_list)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    field = [
        "username",
        "first_name",
        "last_name",
        "email"
    ]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

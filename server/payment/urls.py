from django.urls import path
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name="success"),
    path('billing_info', views.billing_info, name="bill_info"),
    path('add_funds', views.add_funds, name='add_funds'),
    path('process', views.processing, name='process_payment')
]

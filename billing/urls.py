from django.urls import path

from billing.views import payment_method_view,payment_create_view

app_name = 'billing'

urlpatterns = [
    path('payment-method/', payment_method_view, name='payment_method'),
    path('payment-method/create', payment_create_view, name='payment_method_endpoint'),
]

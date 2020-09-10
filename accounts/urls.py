from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import LoginView,RegisterView,guest_register_view

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

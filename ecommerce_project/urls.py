"""ecommerce_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from products import views
from accounts.views import guest_register_view
from address.views import checkout_address_create,checkout_address_reuse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/guest', guest_register_view, name='guest_register'),
    path('', views.HomepageView.as_view(), name='homepage'),
    path('contact/',views.ContactView.as_view(), name = 'contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('products/',include('products.urls',namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    path('carts/', include('carts.urls', namespace='carts')),
    path('accounts/', include('accounts.urls')),
    path('checkout/address/create/', checkout_address_create, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse, name='checkout_address_reuse'),

]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

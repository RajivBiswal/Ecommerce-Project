from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
        path('',views.ProductListView.as_view(), name='list'),
        path('<slug:the_slug>/', views.ProductSlugDetailView.as_view(), name ='detail'),
]

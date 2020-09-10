from django.urls import path

from search import views

app_name = 'search'


urlpatterns = [
    path('',views.SearchProductView.as_view(),name='query'),

]

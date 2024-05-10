from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('search', search_view, name='search_view'),
    path('about', about_view, name='about'),
]

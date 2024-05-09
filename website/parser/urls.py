from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('search', search_view, name='search_view'),
    #path('category/<str:category_name>/', search_by_category, name='category_view'),
]

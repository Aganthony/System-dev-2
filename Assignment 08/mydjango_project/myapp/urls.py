# urls.py

from django.urls import path
from .views import create_bookmark

urlpatterns = [
    path('bookmarks/create/', create_bookmark, name='create-bookmark'),
  
]

from django.urls import path
from .views import index, reactorPage

urlpatterns = [
    path('', index),
    path('reactor/<int:reactor_id>', reactorPage)
]
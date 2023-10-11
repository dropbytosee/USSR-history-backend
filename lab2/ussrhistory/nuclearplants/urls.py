from django.urls import path

from nuclearplants.views import *

urlpatterns = [
    path('', index, name="home"),
    path('spare/<int:reactor_id>', reactor_details, name="reactor_details"),
    path('spare/<int:reactor_id>/delete/', reactor_delete, name="reactor_delete"),
]

from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/reactors/search/', search_reactors),  # GET
    path('api/reactors/<int:reactor_id>/', get_reactor_by_id),  # GET
    path('api/reactors/<int:reactor_id>/image/', get_reactor_image),  # GET
    path('api/reactors/<int:reactor_id>/update/', update_reactor),  # PUT
    path('api/reactors/<int:reactor_id>/update_image/', update_reactor_image),  # PUT
    path('api/reactors/<int:reactor_id>/delete/', delete_reactor),  # DELETE
    path('api/reactors/create/', create_reactor),  # POST
    path('api/reactors/<int:reactor_id>/add_to_station/', add_reactor_to_station),  # POST

    # Набор методов для заявок
    path('api/stations/search/', search_stations),  # GET
    path('api/stations/<int:station_id>/', get_station_by_id),  # GET
    path('api/stations/<int:station_id>/update/', update_station),  # PUT
    path('api/stations/<int:station_id>/update_year/', update_station_year),  # PUT
    path('api/stations/<int:station_id>/update_status_user/', update_status_user),  # PUT
    path('api/stations/<int:station_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/stations/<int:station_id>/delete/', delete_station),  # DELETE
    path('api/stations/<int:station_id>/delete_reactor/<int:reactor_id>/', delete_reactor_from_station), # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]

from datetime import datetime

import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_station(request):
    user = identity_user(request)

    if user is None:
        return None

    station = Station.objects.filter(owner_id=user.id).filter(status=1).first()

    return station


@api_view(["GET"])
def search_reactors(request):
    query = request.GET.get("query", "")

    reactor = Reactor.objects.filter(status=1).filter(name__icontains=query)

    serializer = ReactorSerializer(reactor, many=True)

    draft_station = get_draft_station(request)

    resp = {
        "reactors": serializer.data,
        "draft_station_id": draft_station.pk if draft_station else None
    }

    return Response(resp)


@api_view(["GET"])
def get_reactor_by_id(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)
    serializer = ReactorSerializer(reactor, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_reactor(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)
    serializer = ReactorSerializer(reactor, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_reactor(request):
    reactor = Reactor.objects.create()

    serializer = ReactorSerializer(reactor)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_reactor(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)
    reactor.status = 5
    reactor.save()

    reactor = Reactor.objects.filter(status=1)
    serializer = ReactorSerializer(reactor, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_reactor_to_station(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)

    station = get_draft_station(request)

    if station is None:
        station = Station.objects.create()

    if station.reactors.contains(reactor):
        return Response(status=status.HTTP_409_CONFLICT)

    station.reactors.add(reactor)
    station.owner = identity_user(request)
    station.save()

    serializer = StationSerializer(station)
    return Response(serializer.data)


@api_view(["GET"])
def get_reactor_image(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)

    return HttpResponse(reactor.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_reactor_image(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)
    serializer = ReactorSerializer(reactor, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_stations(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start", -1)
    date_end = request.GET.get("date_end", -1)

    stations = Station.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        stations = stations.filter(owner=user)

    if status_id != -1:
        stations = stations.filter(status=status_id)

    if date_start:
        stations = stations.filter(date_formation__gte=parse_datetime(date_start))

    if date_end:
        stations = stations.filter(date_formation__lt=parse_datetime(date_end))

    serializer = StationsSerializer(stations, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_station_by_id(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    station = Station.objects.get(pk=station_id)
    serializer = StationSerializer(station, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_station(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    station = Station.objects.get(pk=station_id)
    serializer = StationSerializer(station, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_station_year(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    station = Station.objects.get(pk=station_id)
    serializer = StationSerializer(station, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    station = Station.objects.get(pk=station_id)

    station.status = 2
    station.date_formation = timezone.now()
    station.save()

    calculate_opening_year(station_id)

    serializer = StationSerializer(station, many=False)

    return Response(serializer.data)


def calculate_opening_year(station_id):
    data = {
        "station_id": station_id
    }

    requests.post("http://127.0.0.1:8080/calc_year/", json=data, timeout=3)



@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    station = Station.objects.get(pk=station_id)

    if station.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    station.status = request_status
    station.date_complete = timezone.now()
    station.save()

    serializer = StationSerializer(station, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_station(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    station = Station.objects.get(pk=station_id)

    if station.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    station.status = 5
    station.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_reactor_from_station(request, station_id, reactor_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    station = Station.objects.get(pk=station_id)
    station.reactors.remove(Reactor.objects.get(pk=reactor_id))
    station.save()

    if station.reactors.count() == 0:
        station.delete()
        return Response(status=status.HTTP_201_CREATED)

    serializer = StationSerializer(station)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован!',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response

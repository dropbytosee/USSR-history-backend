from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import *


@api_view(["GET"])
def search_reactors(request):
    query = request.GET.get("query")

    reactors = Reactor.objects.filter(status=1).filter(name__icontains=query)

    serializer = ReactorSerializer(reactors, many=True)

    data = {
        "reactors": serializer.data
    }

    return Response(data)


@api_view(["GET"])
def get_reactor_by_id(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(f"Реактора с таким id не существует!")

    reactor = Reactor.objects.get(pk=reactor_id)
    serializer = ReactorSerializer(reactor, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_reactor(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(f"Реактора с таким id не существует!")

    reactor = Reactor.objects.get(pk=reactor_id)
    serializer = ReactorSerializer(reactor, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_reactor(request):
    Reactor.objects.create()

    reactors = Reactor.objects.all()
    serializer = ReactorSerializer(reactors, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_reactor(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(f"Реактора с таким id не существует!")

    reactor = Reactor.objects.get(pk=reactor_id)
    reactor.status = 2
    reactor.save()

    reactors = Reactor.objects.filter(status=1)
    serializer = ReactorSerializer(reactors, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_reactor_to_station(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(f"Реактора с таким id не существует!")

    reactor = Reactor.objects.get(pk=reactor_id)

    station = Station.objects.filter(status=1).last()

    if station is None:
        station = Station.objects.create()

    station.reactors.add(reactor)
    station.save()

    serializer = ReactorSerializer(station.reactors, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_reactor_image(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)

    return HttpResponse(reactor.image, content_type="image/png")


@api_view(["PUT"])
def update_reactor_image(request, reactor_id):
    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    reactor = Reactor.objects.get(pk=reactor_id)
    serializer = ReactorSerializer(reactor, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)




@api_view(["GET"])
def get_stations(request):
    stations = Station.objects.all()
    serializer = StationSerializer(stations, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_station_by_id(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(f"Электростанции с таким id не существует!")

    station = Station.objects.get(pk=station_id)
    serializer = StationSerializer(station, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def update_station(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(f"Электростанции с таким id не существует!")

    station = Station.objects.get(pk=station_id)
    serializer = StationSerializer(station, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    station.status = 1
    station.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(f"Электростанции с таким id не существует!")

    request_status = request.data["status"]

    if request_status not in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    station = Station.objects.get(pk=station_id)
    lesson_status = station.status

    if lesson_status == 5:
        return Response("Статус изменить нельзя")

    station.status = request_status
    station.save()

    serializer = StationSerializer(station, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(f"Электростанции с таким id не существует!")

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    station = Station.objects.get(pk=station_id)

    lesson_status = station.status

    if lesson_status in [3, 4, 5]:
        return Response("Статус изменить нельзя")

    station.status = request_status
    station.save()

    serializer = StationSerializer(station, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_station(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(f"Электростанции с таким id не существует!")

    station = Station.objects.get(pk=station_id)
    station.status = 5
    station.save()

    stations = Station.objects.all()
    serializer = StationSerializer(stations, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_reactor_from_station(request, station_id, reactor_id):
    if not Station.objects.filter(pk=station_id).exists():
        return Response(f"Электростанции с таким id не существует")

    if not Reactor.objects.filter(pk=reactor_id).exists():
        return Response(f"Реактора с таким id не существует")

    station = Station.objects.get(pk=station_id)
    station.reactors.remove(Reactor.objects.get(pk=reactor_id))
    station.save()

    serializer = ReactorSerializer(station.reactors, many=True)
    return Response(serializer.data)


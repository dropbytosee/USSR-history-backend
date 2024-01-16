from rest_framework import serializers

from .models import *


class ReactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactor
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    reactors = ReactorSerializer(read_only=True, many=True)

    class Meta:
        model = Station
        fields = "__all__"


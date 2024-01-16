from rest_framework import serializers

from .models import *


class ReactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactor
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator')


class TicketSerializer(serializers.ModelSerializer):
    reactors = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_reactors(self, ticket):
        if "ids_only" in self.context:
            return [reactor["id"] for reactor in ReactorSerializer(ticket.reactors, many=True).data]

        serializer = ReactorSerializer(ticket.reactors, read_only=True, many=True)
        return serializer.data

    class Meta:
        model = Station
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
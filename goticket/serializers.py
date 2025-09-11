from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = "__all__"



class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"



class ConsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = "__all__"


class SingerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Singer
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta :
        model = City
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta :
        model = Ticket
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields ="__all__"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # ✅ Hash the password
        return super().create(validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

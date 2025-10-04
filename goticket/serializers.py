from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = [
            'sport_name',
            'photo',
        ]



class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            'club_name',
            'photo',
            'event_time',
            'event_date',
        ]



class ConsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = [
            'concert_name',
            'photo',
        ]


class SingerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Singer
        fields = [
            'singer_name',
            'event_time',
            'event_date',
            'photo',
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta :
        model = City
        fields = [
            'city_name',
            'photo',
        ]


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'place_name',
            'photo',
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta :
        model = Ticket
        fields = [
            'category',
            'price',
            'seat_number',
            
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = [
            "password",
            "email",
            "full_name",
            "phone",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # ✅ Hash the password
        return super().create(validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

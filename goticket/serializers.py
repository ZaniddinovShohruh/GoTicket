from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import *


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = [
            'sport_id',
            'sport_name',
            'photo',
        ]
        read_only_fields = ['sport_id']


class ClubSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source='places.place_name', read_only=True)
    place_capacity = serializers.IntegerField(source='places.capacity', read_only=True)

    class Meta:
        model = Club
        fields = [
            'club_id',
            'club_name',
            'photo',
            'event_time',
            'event_date',
            'cities',
            'places',
            'place_name',
            'place_capacity',
            'sports',
        ]
        read_only_fields = ['club_id', 'place_name', 'place_capacity']


class ConsertSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source='places.place_name', read_only=True)
    place_capacity = serializers.IntegerField(source='places.capacity', read_only=True)

    class Meta:
        model = Concert
        fields = [
            'concert_id',
            'concert_name',
            'photo',
            'cities',
            'places',
            'place_name',
            'place_capacity',
            'singer',
        ]
        read_only_fields = ['concert_id', 'place_name', 'place_capacity']


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = [
            'singer_id',
            'singer_name',
            'event_time',
            'event_date',
            'photo',
        ]
        read_only_fields = ['singer_id']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'city_id',
            'city_name',
            'photo',
        ]
        read_only_fields = ['city_id']


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'place_id',
            'place_name',
            'photo',
            'city',
            'capacity',
            'scheme',
        ]
        read_only_fields = ['place_id', 'capacity']


# chipta ichida ko'rsatiladigan tadbir ma'lumotlari (Club yoki Concert)
def event_info(event):
    if event is None:
        return None

    if isinstance(event, Club):
        event_type = 'club'
        date = event.event_date
        time = event.event_time
        extra = event.sports.sport_name if event.sports else None
    else:
        event_type = 'concert'
        date = event.singer.event_date
        time = event.singer.event_time
        extra = event.singer.singer_name

    return {
        'name': str(event),
        'type': event_type,
        'date': date.isoformat() if date else None,
        'time': time.isoformat() if time else None,
        'place': event.places.place_name,
        'city': event.cities.city_name,
        'extra': extra,
        'photo': event.photo.url if event.photo else None,
    }


class TicketSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()
    event_id = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    row = serializers.SerializerMethodField()
    seat = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'ticket_id',
            'category',
            'price',
            'currency',
            'seat_number',
            'section',
            'row',
            'seat',
            'is_sold',
            'buyer',
            'purchased_at',
            'event_type',
            'event_id',
            'event_name',
            'event',
        ]
        read_only_fields = fields

    def get_event(self, obj):
        return event_info(obj.event)

    def get_section(self, obj):
        return obj.seat.section.name if obj.seat_id else None

    def get_row(self, obj):
        return obj.seat.row if obj.seat_id else None

    def get_seat(self, obj):
        return obj.seat.number if obj.seat_id else None

    def get_event_type(self, obj):
        return obj.content_type.model  # 'club' yoki 'concert'

    def get_event_id(self, obj):
        return obj.object_id

    def get_event_name(self, obj):
        if obj.event is None:
            return 'Unknown event'
        return str(obj.event)


# API orqali chipta yaratish: event_type ('club' yoki 'concert') + event_id
class TicketCreateSerializer(serializers.ModelSerializer):
    event_type = serializers.ChoiceField(choices=['club', 'concert'], write_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ticket
        fields = [
            'ticket_id',
            'category',
            'price',
            'currency',
            'seat_number',
            'event_type',
            'event_id',
        ]
        read_only_fields = ['ticket_id']

    def create(self, validated_data):
        event_type = validated_data.pop('event_type')
        event_id = validated_data.pop('event_id')

        if event_type == 'club':
            ct = ContentType.objects.get_for_model(Club)
        else:
            ct = ContentType.objects.get_for_model(Concert)

        # tadbir borligi va o'rindiq bandligini model o'zi tekshiradi (Ticket.clean)
        try:
            return Ticket.objects.create(content_type=ct, object_id=event_id, **validated_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        except IntegrityError:
            raise serializers.ValidationError({'seat_number': 'This seat is already taken for this event.'})


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['category', 'price', 'currency', 'seat_number']

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        except IntegrityError:
            raise serializers.ValidationError({'seat_number': 'This seat is already taken for this event.'})


class TicketTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTariff
        fields = ['category', 'price', 'currency']


class TicketSeatBuySerializer(serializers.Serializer):
    event_type = serializers.ChoiceField(choices=['club', 'concert'])
    event_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'email',
            'full_name',
            'phone',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        phone = validated_data.get('phone')
        if phone == '':
            validated_data['phone'] = None
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

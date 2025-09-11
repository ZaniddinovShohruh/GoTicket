from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('sport_id', 'sport_name','created_at','updated_at')
    list_filter = ('sport_name', 'sport_id',)
    readonly_fields = ('created_at', 'updated_at') # admin ham ozagrtirib bolmas fieldlar 
    fieldsets = (
        ("Asosiy ma`lumotlar", {
            "fields": ("sport_name",),
        }),
    )
    search_fields = ('sport_name',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_id', 'event_time','club_name','event_date','updated_at','created_at')
    list_filter = ('event_time', 'club_name','event_date',)
    readonly_fields = ('created_at','updated_at')
    fieldsets = (
        ("Asosiy ma`lumotlar", {
            "fields": ('event_time','club_name','event_date'),
        }),
    )
    search_fields = ('club_name','event_date','event_time',)


@admin.register(Concert)
class ConsertAdmin(admin.ModelAdmin):
    list_display = ('concert_name','concert_id','created_at','updated_at')
    list_filter = ('concert_name', 'concert_id',)
    readonly_fields = ('created_at','updated_at')
    search_fields = ('concert_name',)

    fieldsets = (
        ("Asosiy ma`lumotlar", {
            'fields': ('concert_name',),
        }),
    )
    
@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ('singer_name','singer_id','event_time','event_date','created_at','updated_at')
    list_filter = ('singer_name','event_time','event_date','singer_id',)
    readonly_fields =  ('created_at','updated_at')
    search_fields = ('singer_name','event_time','event_date',)

    fieldsets = (
        ('Asosiy ma`lumotlar', {
            'fields': ('singer_name','event_time','event_date'),
        }),
    )

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name','city_id','created_at','updated_at')
    list_filter = ('city_name',)
    readonly_fields = ('created_at','updated_at')
    search_fields = ('city_name',)
    fieldsets = (
        ('Asosiy ma`lumotlar', {
            'fields': ('city_name',),
        }),
    )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('place_name',"place_id", 'created_at','updated_at')
    list_filter = ('place_name',)
    readonly_fields = ('created_at','updated_at')
    search_fields = ("place_name",)

    fieldsets = (
        ( 'Asosiy ma`lumotlar', {
            'fields': ('place_name',),
        }),
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('category','price','seat_number','is_sold')
    list_filter = ('category','price',)

    fieldsets = (
        ('Asosiy ma`lumotlar', {
            'fields': ('category','price','seat_number'),
        }),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "phone", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active",)
    search_fields = ("email", "full_name", "phone")
    readonly_fields = ("last_login",)

    fieldsets = (
        ("Asosiy ma'lumotlar", {"fields": ("email", "full_name", "phone", "password")}),
        ("Ruxsatlar", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Tizim ma'lumotlari", {"fields": ("last_login",)}),
    )


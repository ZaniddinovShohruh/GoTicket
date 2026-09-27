from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import *

admin.site.register([Sport,City,Club,Concert,User,Singer])


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ('name', 'category', 'rows', 'seats_per_row', 'row_layout', 'map_x', 'map_y', 'order', 'seat_count')
    readonly_fields = ('seat_count',)

    @admin.display(description='Seats')
    def seat_count(self, obj):
        return obj.seats.count() if obj.pk else 0


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'city', 'capacity', 'section_count')
    readonly_fields = ('capacity',)
    fields = ('place_name', 'city', 'photo', 'scheme', 'capacity')
    inlines = [SectionInline]

    @admin.display(description='Sections')
    def section_count(self, obj):
        return obj.sections.count()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.refresh_capacity()


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'category', 'rows', 'seats_per_row', 'seat_count')
    list_filter = ('place', 'category')
    search_fields = ('name', 'place__place_name')
    actions = ['regenerate_seats']

    @admin.display(description='Seats')
    def seat_count(self, obj):
        return obj.seats.count()

    @admin.action(description='O‘rindiqlarni qayta yaratish')
    def regenerate_seats(self, request, queryset):
        for section in queryset:
            section.generate_seats()
        self.message_user(request, f'{queryset.count()} ta sektor yangilandi.')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('section', 'row', 'number')
    list_filter = ('section__place', 'section')
    search_fields = ('section__name',)
    list_per_page = 100


# Ticket va TicketTariff uchun umumiy forma: id yozish o'rniga ro'yxatdan Club yoki Concert tanlanadi
class EventChoiceForm(forms.ModelForm):
    club = forms.ModelChoiceField(
        queryset=Club.objects.all().order_by('club_name'),
        required=False,
        label='Club (match)',
        help_text='Match bo‘lsa Club ni tanlang.',
    )
    concert = forms.ModelChoiceField(
        queryset=Concert.objects.all().order_by('concert_name'),
        required=False,
        label='Concert',
        help_text='Konsert bo‘lsa Concert ni tanlang.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tahrirlashda oldin tanlangan tadbirni ko'rsatamiz
        if not self.instance.pk:
            return
        event = self.instance.event
        if isinstance(event, Club):
            self.fields['club'].initial = event
        if isinstance(event, Concert):
            self.fields['concert'].initial = event

    def clean(self):
        cleaned_data = super().clean()
        club = cleaned_data.get('club')
        concert = cleaned_data.get('concert')

        if club and concert:
            raise forms.ValidationError('Faqat Club yoki Concert dan bittasini tanlang.')

        # tanlangan tadbirni content_type va object_id ga yozamiz, model.clean() shularni tekshiradi
        # (hech narsa tanlanmasa "Club yoki Concert tanlang" xatosini model o'zi beradi)
        event = club or concert
        if event:
            self.instance.content_type = ContentType.objects.get_for_model(event)
            self.instance.object_id = event.pk
        else:
            self.instance.content_type = None
        return cleaned_data


class TicketAdminForm(EventChoiceForm):
    class Meta:
        model = Ticket
        fields = ['club', 'concert', 'category', 'price', 'currency', 'seat', 'seat_number']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = TicketAdminForm
    list_display = ('category', 'price', 'currency', 'seat_number', 'is_sold', 'buyer', 'event')
    list_filter = ('category', 'currency', 'is_sold')
    readonly_fields = ('is_sold', 'buyer', 'purchased_at')
    raw_id_fields = ('seat',)
    search_fields = ('seat_number', 'buyer__email')

    fieldsets = (
        ('Event', {
            'fields': ('club', 'concert'),
            'description': 'Chiptani yaratilgan Club (match) yoki Concert ga ulang. Id yozish shart emas.',
        }),
        ('Chipta', {
            'fields': ('category', 'price', 'currency', 'seat', 'seat_number'),
        }),
        ('Sotuv holati', {
            'fields': ('is_sold', 'buyer', 'purchased_at'),
        }),
    )


class TicketTariffAdminForm(EventChoiceForm):
    class Meta:
        model = TicketTariff
        fields = ['club', 'concert', 'category', 'price', 'currency']


@admin.register(TicketTariff)
class TicketTariffAdmin(admin.ModelAdmin):
    form = TicketTariffAdminForm
    list_display = ('category', 'price', 'currency', 'event')
    list_filter = ('category', 'currency')
    fieldsets = (
        ('Event', {
            'fields': ('club', 'concert'),
            'description': 'Avval Place da sektorlarni kiriting (o‘rindiqlar avtomatik yaratiladi), keyin shu tadbir uchun VIP/Standart narx va valyuta qo‘ying. Sektor kategoriyasi shu narxni oladi.',
        }),
        ('Narx', {
            'fields': ('category', 'price', 'currency'),
        }),
    )




# @admin.register(Sport)
# class SportAdmin(admin.ModelAdmin):
#     list_display = ('sport_id', 'sport_name','created_at','updated_at')
#     list_filter = ('sport_name', 'sport_id',)
#     readonly_fields = ('created_at', 'updated_at') # admin ham ozagrtirib bolmas fieldlar 
#     fieldsets = (
#         ("Asosiy ma`lumotlar", {
#             "fields": ("sport_name",),
#         }),
#     )
#     search_fields = ('sport_name',)


# @admin.register(Club)
# class ClubAdmin(admin.ModelAdmin):
#     list_display = ('club_id', 'event_time','club_name','event_date','updated_at','created_at')
#     list_filter = ('event_time', 'club_name','event_date',)
#     readonly_fields = ('created_at','updated_at')
#     fieldsets = (
#         ("Asosiy ma`lumotlar", {
#             "fields": ('event_time','club_name','event_date'),
#         }),
#     )
#     search_fields = ('club_name','event_date','event_time',)


# @admin.register(Concert)
# class ConsertAdmin(admin.ModelAdmin):
#     list_display = ('concert_name','concert_id','created_at','updated_at')
#     list_filter = ('concert_name', 'concert_id',)
#     readonly_fields = ('created_at','updated_at')
#     search_fields = ('concert_name',)

#     fieldsets = (
#         ("Asosiy ma`lumotlar", {
#             'fields': ('concert_name',),
#         }),
#     )
    
# @admin.register(Singer)
# class SingerAdmin(admin.ModelAdmin):
#     list_display = ('singer_name','singer_id','event_time','event_date','created_at','updated_at')
#     list_filter = ('singer_name','event_time','event_date','singer_id',)
#     readonly_fields =  ('created_at','updated_at')
#     search_fields = ('singer_name','event_time','event_date',)

#     fieldsets = (
#         ('Asosiy ma`lumotlar', {
#             'fields': ('singer_name','event_time','event_date'),
#         }),
#     )

# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = ('city_name','city_id','created_at','updated_at')
#     list_filter = ('city_name',)
#     readonly_fields = ('created_at','updated_at')
#     search_fields = ('city_name',)
#     fieldsets = (
#         ('Asosiy ma`lumotlar', {
#             'fields': ('city_name',),
#         }),
#     )


# @admin.register(Place)
# class PlaceAdmin(admin.ModelAdmin):
#     list_display = ('place_name',"place_id", 'created_at','updated_at')
#     list_filter = ('place_name',)
#     readonly_fields = ('created_at','updated_at')
#     search_fields = ("place_name",)

#     fieldsets = (
#         ( 'Asosiy ma`lumotlar', {
#             'fields': ('place_name',),
#         }),
#     )


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('category','price','seat_number','is_sold')
#     list_filter = ('category','price',)

#     fieldsets = (
#         ('Asosiy ma`lumotlar', {
#             'fields': ('category','price','seat_number'),
#         }),
#     )


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ( "email", "full_name", "phone", "is_staff", "is_active")
#     list_filter = ("is_staff", "is_active",)
#     search_fields = ("email", "full_name", "phone")
#     readonly_fields = ("last_login",)

#     fieldsets = (
#         ("Asosiy ma'lumotlar", {"fields": ("email", "full_name", "phone", "password")}),
#         ("Ruxsatlar", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
#         ("Tizim ma'lumotlari", {"fields": ("last_login",)}),
    #  )
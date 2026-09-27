from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.models import ContentType #bitta modelni hamma modelga ulash uchun ishlatiladi va hamma modelni bitta ContentType obyekt qilib saqlaydi 
from django.contrib.contenttypes.fields import GenericForeignKey #bir nechta modelga bir xil field orqali ulanadi, ForeignKey faqat bitta modelga ulanadi va kop modellarni ulash kere bosa kop FK yozish kere , bu bilan faqat bitta shu yoziladi va bitta qator kod bilan bir necha qator FK yoziladi 

# chipta faqat shu ikki modelga ulanadi
TICKET_EVENT_MODELS = ('club', 'concert')

CATEGORY_CHOICES = (
    ('VIP', 'VIP'),
    ('Standart', 'Standart'),
)

CURRENCY_CHOICES = (
    ('USD', 'Dollar ($)'),
    ('EUR', 'Euro (€)'),
    ('UZS', "So'm"),
)


# admin panelda content_type ro'yxatida faqat Club va Concert chiqadi (migratsiyalarda ishlatilgan, nomini o'zgartirmang)
def limit_ticket_content_type():
    return models.Q(app_label='goticket', model__in=TICKET_EVENT_MODELS)


# "  A1 " -> "A1", bo'sh qiymat -> None
def normalize_seat_number(value):
    if value is None:
        return None
    value = str(value).strip()
    if value == '':
        return None
    return value




class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)   
    sport_name = models.CharField(max_length=100,db_index=True, verbose_name='Type of sport')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    photo = models.ImageField(upload_to='photos/sport_photo/', blank=True, null=True)

    class Meta:
        verbose_name='Sport'
        verbose_name_plural ='Sports'

        indexes = [
            models.Index(fields=['sport_name'], name = 'sport_name_index')
        ]

    def __str__(self):
        return self.sport_name 

class Club(models.Model):
    club_id = models.AutoField(primary_key=True, verbose_name='Club id')
    event_time = models.DateField(verbose_name='Event time')
    club_name = models.CharField(max_length=200,db_index=True, verbose_name='Club name')
    event_date = models.DateField(verbose_name='Event data')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    photo = models.ImageField(upload_to='photos/club_photo/', blank=True, null=True)
    cities = models.ForeignKey('City', related_name='clubs', on_delete=models.CASCADE)
    places = models.ForeignKey('Place',on_delete=models.CASCADE, related_name='clubs')
    sports = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='clubs', null=True, blank=True)

    class Meta:
        verbose_name='Club'
        verbose_name_plural = 'Clubs'

        indexes = [
            models.Index(fields=['club_name', 'event_date', 'event_time'], name = 'name_time_date_index')
        ]

    def __str__(self):
        return self.club_name



class Concert(models.Model):
    concert_name = models.CharField(max_length=200,db_index=True, verbose_name='Consert name')
    concert_id = models.AutoField(primary_key=True, verbose_name='Consert id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    cities = models.ForeignKey('City', related_name='conserts', on_delete=models.CASCADE)
    places = models.ForeignKey('Place', on_delete = models.CASCADE ,related_name='conserts')
    singer = models.ForeignKey('Singer', on_delete=models.CASCADE, related_name='conserts' )
    photo = models.ImageField(upload_to='photos/concert_photo/', blank=True, null=True)

    class Meta:
        verbose_name = 'Concert'
        verbose_name_plural = 'Concerts'

        indexes = [
            models.Index(fields=['concert_name'], name = 'concert_name_index')
        ]
    
    def __str__(self):
        return self.concert_name



class Singer(models.Model):
    singer_id = models.AutoField(primary_key=True, verbose_name='Singer id')
    singer_name = models.CharField(max_length=200, db_index=True, verbose_name='Singer name')
    event_time = models.TimeField(verbose_name='Event time')
    event_date = models.DateField(verbose_name='Event data')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    photo = models.ImageField(upload_to='photos/singer_photo/', blank=True, null=True)

    class Meta:
        verbose_name = 'Singer'
        verbose_name_plural = 'Singers'

        indexes = [
            models.Index(fields=['singer_name','event_time','event_date'], name = 'singer_event_time_date_index')
        ]

    def __str__(self):
        return self.singer_name
    

class City(models.Model):
    city_name = models.CharField(max_length=200, db_index=True, verbose_name='City name')  #db_index=True databaseni tartiblaydi va bu qidirishni tezlashtiradi, agar buni qoymasak ketma-ket qidiradi va bu ishlashni seknlashtiradi
    city_id = models.AutoField(primary_key=True, verbose_name='City id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    photo = models.ImageField(upload_to='photos/city_photo/', blank=True, null=True)

    class Meta :
     verbose_name = 'City'
     verbose_name_plural = 'Cities'

     indexes = [       # admin pagedan ma`lumot qidirganda kop funksiya bajarmasdan faqat kiritgan fielda oid malumotni chiqaradi va bu boshqa funksiyalarni sekinlashtirmaydi va tezroq ishlshiga yordam beradi.
         models.Index(fields=['city_name'], name = 'city_name_index')
     ]

    def __str__(self): # bu admin pageda database ochilganda ichidagi qoshilgan narsala kornmidi va bu funksiya yordamidi korinadi 
        return self.city_name

class Place(models.Model):
    place_id = models.AutoField(primary_key=True, verbose_name='Place id')
    place_name = models.TextField(max_length=200, verbose_name='Place name', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    photo = models.ImageField(upload_to='photos/place_photo/', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='places')
    scheme = models.ImageField(
        upload_to='photos/place_scheme/',
        blank=True,
        null=True,
        verbose_name='Stadium scheme',
        help_text='Stadion sxemasi rasmi (sektorlar ko‘rinadigan rasm)',
    )
    capacity = models.PositiveIntegerField(
        default=0,
        verbose_name='Seat capacity',
        help_text='Sektorlardagi o‘rindiqlardan avtomatik hisoblanadi',
    )


    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'


        indexes = [
            models.Index(fields=['place_name'], name='place_name_index')
        ]

    def __str__(self):
        return self.place_name

    def refresh_capacity(self):
        self.capacity = Seat.objects.filter(section__place=self).count()
        Place.objects.filter(pk=self.pk).update(capacity=self.capacity)


# "20,22,24" -> [20, 22, 24]  (1-qatorda 20 ta, 2-qatorda 22 ta, 3-qatorda 24 ta o'rindiq)
def parse_row_layout(value):
    counts = []
    if not value:
        return counts

    for part in value.split(','):
        part = part.strip()
        if part == '':
            continue
        if not part.isdigit() or int(part) == 0:
            raise ValidationError({'row_layout': 'Faqat musbat sonlar, vergul bilan: masalan 20,22,24'})
        counts.append(int(part))
    return counts


class Section(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=20, verbose_name='Section name', help_text='Masalan A401, B408, Fan-zona')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Standart',
        verbose_name='category',
    )
    rows = models.PositiveIntegerField(default=10, verbose_name='Rows')
    seats_per_row = models.PositiveIntegerField(default=20, verbose_name='Seats per row')
    row_layout = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Row layout',
        help_text='Ixtiyoriy: har qatordagi o‘rindiqlar soni vergul bilan (20,22,24). To‘ldirilsa Rows va Seats per row o‘rniga ishlatiladi.',
    )
    map_x = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Map X %',
        help_text='Sxema rasmida sektor joyi: chapdan foizda (0–100)',
    )
    map_y = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Map Y %',
        help_text='Sxema rasmida sektor joyi: tepadan foizda (0–100)',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Order')

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['order', 'name']
        constraints = [
            models.UniqueConstraint(fields=['place', 'name'], name='unique_place_section'),
        ]

    def __str__(self):
        return f'{self.place} — {self.name}'

    # har qatorda nechta o'rindiq borligi: [20, 20, 20] yoki row_layout dan [20, 22, 24]
    def row_counts(self):
        layout = parse_row_layout(self.row_layout)
        if layout:
            return layout
        return [self.seats_per_row] * self.rows

    def clean(self):
        if sum(self.row_counts()) == 0:
            raise ValidationError('Sektorda kamida bitta o‘rindiq bo‘lishi kerak.')
        if self.map_x is not None and not (0 <= self.map_x <= 100):
            raise ValidationError({'map_x': '0 dan 100 gacha bo‘lishi kerak.'})
        if self.map_y is not None and not (0 <= self.map_y <= 100):
            raise ValidationError({'map_y': '0 dan 100 gacha bo‘lishi kerak.'})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_seats()

    # sektor saqlanganda o'rindiqlarni avtomatik yaratadi
    def generate_seats(self):
        # kerak bo'lgan o'rindiqlar: (qator, raqam)
        needed = set()
        row = 1
        for count in self.row_counts():
            for number in range(1, count + 1):
                needed.add((row, number))
            row += 1

        # bazada allaqachon bor o'rindiqlar
        existing = {}
        for seat in self.seats.all():
            existing[(seat.row, seat.number)] = seat

        # yetishmayotganlarini yaratamiz
        new_seats = []
        for row, number in sorted(needed):
            if (row, number) not in existing:
                new_seats.append(Seat(section=self, row=row, number=number))
        Seat.objects.bulk_create(new_seats, batch_size=2000)

        # ortiqchalarini o'chiramiz, lekin chiptasi bor o'rindiqqa tegmaymiz
        extra_ids = []
        for key, seat in existing.items():
            if key not in needed:
                extra_ids.append(seat.pk)
        Seat.objects.filter(pk__in=extra_ids, tickets__isnull=True).delete()

        self.place.refresh_capacity()


class Seat(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField(verbose_name='Row')
    number = models.PositiveIntegerField(verbose_name='Seat number')

    class Meta:
        verbose_name = 'Seat'
        verbose_name_plural = 'Seats'
        ordering = ['section', 'row', 'number']
        constraints = [
            models.UniqueConstraint(fields=['section', 'row', 'number'], name='unique_section_seat'),
        ]

    def __str__(self):
        return f'{self.section.name}, {self.row}-qator, {self.number}-o‘rin'

    @property
    def code(self):
        return f'{self.section.name}-{self.row}-{self.number}'




class Ticket(models.Model):
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Standart',
        verbose_name='category',
    ) 
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price')
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='UZS',
        verbose_name='Currency',
    )
    seat = models.ForeignKey(
        'Seat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name='Seat',
    )
    seat_number = models.CharField(max_length=40, blank=True, null=True, verbose_name='Seat number')  
    is_sold = models.BooleanField(default=False)
    ticket_id = models.AutoField(primary_key=True, verbose_name='Ticket id')
    buyer = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchased_tickets',
    )
    purchased_at = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=limit_ticket_content_type,
    )
    object_id = models.PositiveIntegerField()
    event = GenericForeignKey("content_type", "object_id")

    def clean(self):
        self.seat_number = normalize_seat_number(self.seat_number)

        # content_type va object_id admin formasida yo'q, shuning uchun xatolar field nomisiz beriladi
        if not self.content_type_id:
            raise ValidationError('Club yoki Concert tanlang.')
        if self.content_type.model not in TICKET_EVENT_MODELS:
            raise ValidationError('Chipta faqat Club yoki Concert ga ulanadi.')

        # self.event keshlangan eski qiymatni qaytarishi mumkin, shuning uchun bazadan olamiz
        model = self.content_type.model_class()
        event = model.objects.filter(pk=self.object_id).first()
        if event is None:
            raise ValidationError('Tadbir topilmadi.')

        if self.seat_id and self.seat.section.place_id != event.places_id:
            raise ValidationError({'seat': 'Bu o‘rindiq tadbir o‘tadigan stadionga tegishli emas.'})

        if self.seat_number:
            same_seat = Ticket.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                seat_number=self.seat_number,
            ).exclude(pk=self.pk)
            if same_seat.exists():
                raise ValidationError({'seat_number': 'This seat is already taken for this event.'})

    def save(self, *args, **kwargs):
        if self.seat_id and not self.seat_number:
            self.seat_number = self.seat.code
        self.seat_number = normalize_seat_number(self.seat_number)

        # update_fields bilan saqlash (masalan sotib olish) faqat bir nechta fieldni o'zgartiradi, to'liq tekshiruv shart emas
        if kwargs.get('update_fields') is None:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event} - {self.category} ({'Sold' if self.is_sold else 'Available'})"

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'seat_number'],
                condition=models.Q(seat_number__isnull=False),
                name='unique_seat',
            ),
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'seat'],
                condition=models.Q(seat__isnull=False),
                name='unique_ticket_seat',
            ),
        ]

        indexes = [
            models.Index(fields=['category'], name='category_index'),
            models.Index(fields=['content_type', 'object_id'], name='ticket_event_index'),
        ]


class TicketTariff(models.Model):
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Standart',
        verbose_name='category',
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price')
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='UZS',
        verbose_name='Currency',
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=limit_ticket_content_type,
    )
    object_id = models.PositiveIntegerField()
    event = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Ticket tariff'
        verbose_name_plural = 'Ticket tariffs'
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'category'],
                name='unique_event_tariff',
            )
        ]

    def clean(self):
        if not self.content_type_id:
            raise ValidationError('Club yoki Concert tanlang.')
        if self.content_type.model not in TICKET_EVENT_MODELS:
            raise ValidationError('Narx faqat Club yoki Concert ga qo‘yiladi.')
        model = self.content_type.model_class()
        if not model.objects.filter(pk=self.object_id).exists():
            raise ValidationError('Tadbir topilmadi.')

    def save(self, *args, **kwargs):
        if kwargs.get('update_fields') is None:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.event} — {self.category} ({self.price} {self.currency})'

 


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email Required')
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')
        
            return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name='Full name', db_index=True )
    phone = models.CharField(max_length=200, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/user_photo/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


        indexes = [
            models.Index(fields=['full_name', 'phone', 'email'], name='name_phone_email_index')
        ]


    def __str__(self):
            return self.email


# GenericForeignKey CASCADE qilmaydi: Club yoki Concert o'chirilsa, uning chiptalari va narxlarini qo'lda o'chiramiz
@receiver(pre_delete, sender=Club)
@receiver(pre_delete, sender=Concert)
def delete_event_tickets(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(sender)
    Ticket.objects.filter(content_type=ct, object_id=instance.pk).delete()
    TicketTariff.objects.filter(content_type=ct, object_id=instance.pk).delete()

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.models import ContentType #bitta modelni hamma modelga ulash uchun ishlatiladi va hamma modelni bitta ContentType obyekt qilib saqlaydi 
from django.contrib.contenttypes.fields import GenericForeignKey #bir nechta modelga bir xil field orqali ulanadi, ForeignKey faqat bitta modelga ulanadi va kop modellarni ulash kere bosa kop FK yozish kere , bu bilan faqat bitta shu yoziladi va bitta qator kod bilan bir necha qator FK yoziladi 




class Sport(models.Model):
    sport_id = models.CharField(max_length=200)
    sport_name = models.CharField(max_length=100,db_index=True, verbose_name='Type of sport')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    cities = models.ManyToManyField('City', related_name='sports')
    photo = models.ImageField(upload_to='sport_photo/', blank=True, null=True)

    class Meta:
        verbose_name='Sport'
        verbose_name_plural ='Sports'

        indexes = [
            models.Index(fields=['sport_name'], name = 'sport_name_index')
        ]

    def __str__(self):
        return self.sport_name 



class Club(models.Model):
    club_id = models.CharField(max_length=200, verbose_name='Club id')
    event_time = models.DateField(verbose_name='Event time')
    club_name = models.CharField(max_length=200,db_index=True, verbose_name='Club name')
    event_date = models.DateField(verbose_name='Event data')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='sports')
    photo = models.ImageField(upload_to='club_photo/', blank=True, null=True)
    

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
    concert_id = models.CharField(max_length=200, verbose_name='Consert id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    cities = models.ManyToManyField('City', related_name='conserts')
    photo = models.ImageField(upload_to='concert_photo/', blank=True, null=True)

    class Meta:
        verbose_name = 'Concert'
        verbose_name_plural = 'Concerts'

        indexes = [
            models.Index(fields=['concert_name'], name = 'concert_name_index')
        ]
    
    def __str__(self):
        return self.concert_name



class Singer(models.Model):
    singer_id = models.CharField(max_length=200, verbose_name='Singer id')
    singer_name = models.CharField(max_length=200, db_index=True, verbose_name='Singer name')
    event_time = models.DateField(verbose_name='Event time')
    event_date = models.DateField(verbose_name='Event data')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    consert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='singers') 
    photo = models.ImageField(upload_to='singer_photo/', blank=True, null=True)

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
    city_id = models.CharField(max_length=200, verbose_name='City id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    photo = models.ImageField(upload_to='city_photo/', blank=True, null=True)

    class Meta :
     verbose_name = 'City'
     verbose_name_plural = 'Cities'

     indexes = [       # admin pagedan ma`lumot qidirganda kop funksiya bajarmasdan faqat kiritgan fielda oid malumotni chiqaradi va bu boshqa funksiyalarni sekinlashtirmaydi va tezroq ishlshiga yordam beradi.
         models.Index(fields=['city_name'], name = 'city_name_index')
     ]

    def __str__(self): # bu admin pageda database ochilganda ichidagi qoshilgan narsala kornmidi va bu funksiya yordamidi korinadi 
        return self.city_name

class Place(models.Model):
    place_id = models.CharField(max_length=200, verbose_name='Place id')
    place_name = models.TextField(max_length=200, verbose_name='Place name', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='places')
    photo = models.ImageField(upload_to='place_photo/', blank=True)


    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'


        indexes = [
            models.Index(fields=['place_name'], name='place_name_index')
        ]

    def __str__(self):
        return self.place_name
    



class Ticket(models.Model):
    category = models.CharField(max_length=100, verbose_name='category') 
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price')
    seat_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Seat number')  
    is_sold = models.BooleanField(default=False)   

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)     #Qaysi modelga ulanadi Sport, Concert va boshqalarini tanlaydi 
    object_id = models.PositiveIntegerField()        # U model ichidagi qaysi obyektga ulanadi (id) tanlaydi 
    event = GenericForeignKey("content_type", "object_id")          # Ularni birlashtiradi

    def __str__(self):
        return f"{self.event} - {self.category} ({'Sold' if self.is_sold else 'Available'})"

    

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

        constraints = [   # bu faqat bitta bolishini taminlaydi masalan bizga seat_number va bu tabdir  bitta bolishi kerak va shu tadbirga tegisgli o`rindiq bolishi kerak 
            models.UniqueConstraint(fields=['content_type','object_id','seat_number'], name='unique_seat')
        ]

        indexes = [
            models.Index(fields=['category'], name='category_index')
        ]




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
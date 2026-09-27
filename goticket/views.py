from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.prefetch import GenericPrefetch
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend





class SportView(generics.CreateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAdminUser]

class SportListView(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # filter_backend bizaga mator bob xizmat qiladi va ichidagi objectlani ishlatadi 
    filterset_fields = ['sport_name']  # Sport nomini  aniq filter qilish kere
    search_fields = ['sport_name']  # Search qilish text qidirishlar uchun javob beradi football db yozsa user hamma football db yozilganlarini topadi 
    ordering_fields = ['sport_name', 'created_at']  # Tartiblash
    ordering = ['sport_name']  # Default tartiblash uchun kere agarda user xech narsa bermasa

class SportUpdateView(generics.UpdateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class SportDeleteView(generics.DestroyAPIView):
    queryset = Sport.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class ClubView(generics.CreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAdminUser] 


class ClubListView(generics.ListAPIView):
    serializer_class = ClubSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields ={
        'club_id': ['exact'],
        'club_name': ['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith'], # iexact kotta yoki kickina xarflaga qaramasdan qidirish ucun , contains ichda borligini tekshiradi masalan FC bolgan klublar, endwith belgilangan soz bilan tugasa qoshib qidiradi , startswith bu kiritgan soz bilan boshlansa 
        'event_date':['year','month','day'] # date faqat shu sanadagi oyinlar , yillar , oylar, sanasi boyicha qidiradi
    }
    search_fields = ['club_name'] #clubning nomlari boyicha qidiradi 
    ordering_fields = ['club_name', 'created_at']  # foydalanuvchi faqatshu fieldlar boyicah tartiblat oladi 
    ordering = ['club_name','created_at'] #agar foydalanuvchi tartiblamasa default xolartda tartiblaydi 

    def get_queryset(self):
        return Club.objects.select_related('cities', 'places', 'sports').all()



class ClubUpdateView(generics.UpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAdminUser] 

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    
class ClubDeleteView(generics.DestroyAPIView):
    queryset = Club.objects.all()
    permission_classes = [IsAdminUser]
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

    

class ConsertView(generics.CreateAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConsertSerializer
    permission_classes = [IsAdminUser]


class ConsertListView(generics.ListAPIView):
    serializer_class =  ConsertSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields ={
        'concert_id': ['exact'],
        'concert_name' :['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith']      
    }
    search_fields = ['concert_name']
    ordering_fields = ['concert_name','created_at']
    ordering = ['concert_name','created_at']

    def get_queryset(self):
        return Concert.objects.select_related('cities', 'places', 'singer').all()

class ConsertUpdateView(generics.UpdateAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConsertSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
      
class ConsertDeleteView(generics.DestroyAPIView):
    queryset = Concert.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


class SingerView(generics.CreateAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    permission_classes = [IsAdminUser]

class SingerListView(generics.ListAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields ={
        'singer_name':['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith'],
        'event_date' :['year','month','day']
    }
    search_fields = ['singer_name']
    ordering_fields = ['singer_name','created_at']
    ordering = ['singer_name','created_at']

class SingerUpdateView(generics.UpdateAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class SingerDeleteView(generics.DestroyAPIView):
    queryset = Singer.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CityView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'city_name': ['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith']
    }
    search_fields = ['city_name']
    ordering_fields =['city_name','created_at']
    ordering =['city_name','created_at']


class CityUpdateView(generics.UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class CityDeleteView(generics.DestroyAPIView):
    queryset = City.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


    

class PlaceView(generics.CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUser]

class PlaceListView(generics.ListAPIView):
    serializer_class = PlaceSerializer
    # select_related: FK/OneToOne bilan bog'langan modellarni birga oladi

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields ={
        'place_name':['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith']
    }
    search_fields = ['place_name']
    ordering_fields = ['place_name','created_at']
    ordering = ['place_name','created_at']

    def get_queryset(self):
        return Place.objects.select_related('city').all()

class PlaceUpdateView(generics.UpdateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class PlaceDeleteView(generics.DestroyAPIView):
    queryset = Place.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


# chiptalarni tadbiri, o'rindig'i va xaridori bilan birga oladi (har bir chipta uchun alohida so'rov ketmasligi uchun)
def get_tickets_queryset():
    return Ticket.objects.select_related('content_type', 'buyer', 'seat__section').prefetch_related(
        GenericPrefetch('event', [
            Club.objects.select_related('places', 'cities', 'sports'),
            Concert.objects.select_related('places', 'cities', 'singer'),
        ])
    )


# event_type='club' yoki 'concert' bo'yicha tadbirni topadi, topilmasa None
def get_event(event_type, event_id):
    if not str(event_id).isdigit():
        return None
    if event_type == 'club':
        return Club.objects.select_related('places', 'cities', 'sports').filter(pk=event_id).first()
    if event_type == 'concert':
        return Concert.objects.select_related('places', 'cities', 'singer').filter(pk=event_id).first()
    return None


# tadbirdagi shu kategoriya narxi (VIP yoki Standart)
def get_tariff(event, category):
    ct = ContentType.objects.get_for_model(event)
    return TicketTariff.objects.filter(content_type=ct, object_id=event.pk, category=category).first()


class TicketView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAdminUser]

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category', 'seat_number']
    ordering_fields = ['price', 'category', 'ticket_id']
    ordering = ['price', 'ticket_id']

    def get_queryset(self):
        qs = get_tickets_queryset()

        # ?available=1 -> faqat sotilmagan chiptalar
        available = self.request.query_params.get('available')
        if available in ('1', 'true', 'True'):
            qs = qs.filter(is_sold=False)

        # ?event_type=club&event_id=5 -> faqat shu tadbir chiptalari
        event_type = self.request.query_params.get('event_type')
        event_id = self.request.query_params.get('event_id')
        if event_type == 'club' and event_id:
            qs = qs.filter(content_type=ContentType.objects.get_for_model(Club), object_id=event_id)
        if event_type == 'concert' and event_id:
            qs = qs.filter(content_type=ContentType.objects.get_for_model(Concert), object_id=event_id)
        return qs

class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketUpdateSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class TicketDeleteView(generics.DestroyAPIView):
    queryset =Ticket.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TicketBuyView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        # select_for_update: bir vaqtda ikki kishi bitta chiptani sotib ololmasligi uchun qatorni qulflaydi
        ticket = get_object_or_404(Ticket.objects.select_for_update(), pk=pk)

        if ticket.is_sold:
            return Response({'detail': 'Ticket already sold.'}, status=status.HTTP_400_BAD_REQUEST)
        if ticket.event is None:
            return Response({'detail': 'Event is no longer available.'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.is_sold = True
        ticket.buyer = request.user
        ticket.purchased_at = timezone.now()
        ticket.save(update_fields=['is_sold', 'buyer', 'purchased_at'])
        return Response(TicketSerializer(ticket).data)


# tadbir stadionidagi sektorlar: nechta joy bor, nechtasi bo'sh va narxi
class TicketSeatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        event_type = request.query_params.get('event_type')
        event = get_event(event_type, request.query_params.get('event_id'))
        if event is None:
            return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

        place = event.places
        ct = ContentType.objects.get_for_model(event)
        tariffs = TicketTariff.objects.filter(content_type=ct, object_id=event.pk)

        sections = []
        for section in place.sections.all():
            total = section.seats.count()
            sold = section.seats.filter(
                tickets__content_type=ct,
                tickets__object_id=event.pk,
                tickets__is_sold=True,
            ).count()
            tariff = tariffs.filter(category=section.category).first()

            sections.append({
                'id': section.pk,
                'name': section.name,
                'category': section.category,
                'map_x': float(section.map_x) if section.map_x is not None else None,
                'map_y': float(section.map_y) if section.map_y is not None else None,
                'total': total,
                'available': total - sold,
                'price': str(tariff.price) if tariff else None,
                'currency': tariff.currency if tariff else None,
            })

        capacity = 0
        available_count = 0
        for section in sections:
            capacity += section['total']
            available_count += section['available']

        return Response({
            'event_type': event_type,
            'event_id': event.pk,
            'event': event_info(event),
            'place_name': place.place_name,
            'scheme': place.scheme.url if place.scheme else None,
            'capacity': capacity,
            'available_count': available_count,
            'sections': sections,
            'tariffs': TicketTariffSerializer(tariffs, many=True).data,
        })


# bitta sektordagi qatorlar va o'rindiqlar (qaysilari sotilgan)
class SectionSeatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, section_id):
        event = get_event(request.query_params.get('event_type'), request.query_params.get('event_id'))
        if event is None:
            return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

        section = event.places.sections.filter(pk=section_id).first()
        if section is None:
            return Response({'detail': 'Section not found.'}, status=status.HTTP_404_NOT_FOUND)

        ct = ContentType.objects.get_for_model(event)
        sold_ids = set(
            Ticket.objects.filter(
                content_type=ct,
                object_id=event.pk,
                is_sold=True,
                seat__section=section,
            ).values_list('seat_id', flat=True)
        )

        # { 1: [o'rindiqlar], 2: [o'rindiqlar], ... }
        rows = {}
        for seat in section.seats.all():
            if seat.row not in rows:
                rows[seat.row] = []
            rows[seat.row].append({
                'id': seat.pk,
                'number': seat.number,
                'sold': seat.pk in sold_ids,
            })

        rows_list = []
        for row in sorted(rows):
            rows_list.append({'row': row, 'seats': rows[row]})

        tariff = get_tariff(event, section.category)
        return Response({
            'id': section.pk,
            'name': section.name,
            'category': section.category,
            'price': str(tariff.price) if tariff else None,
            'currency': tariff.currency if tariff else None,
            'rows': rows_list,
        })


# foydalanuvchi sxemadan tanlagan o'rindiqni sotib olish
class TicketBuySeatView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = TicketSeatBuySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        event = get_event(data['event_type'], data['event_id'])
        if event is None:
            return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

        seat = Seat.objects.select_for_update().select_related('section').filter(
            pk=data['seat_id'],
            section__place=event.places,
        ).first()
        if seat is None:
            return Response({'detail': 'Bu o‘rindiq tadbir o‘tadigan stadionda yo‘q.'}, status=status.HTTP_400_BAD_REQUEST)

        tariff = get_tariff(event, seat.section.category)
        if tariff is None:
            message = f'Admin {seat.section.category} kategoriyasi uchun narx belgilamagan.'
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        # admin shu o'rindiqqa oldindan chipta yaratgan bo'lishi mumkin
        ct = ContentType.objects.get_for_model(event)
        ticket = Ticket.objects.select_for_update().filter(content_type=ct, object_id=event.pk, seat=seat).first()
        if ticket is not None and ticket.is_sold:
            return Response({'detail': 'Bu o‘rindiq allaqachon sotilgan.'}, status=status.HTTP_400_BAD_REQUEST)
        if ticket is None:
            ticket = Ticket(content_type=ct, object_id=event.pk, seat=seat)

        ticket.seat_number = seat.code
        ticket.category = tariff.category
        ticket.price = tariff.price
        ticket.currency = tariff.currency
        ticket.is_sold = True
        ticket.buyer = request.user
        ticket.purchased_at = timezone.now()
        try:
            ticket.save()
        except (IntegrityError, DjangoValidationError):
            return Response({'detail': 'Bu o‘rindiq allaqachon sotilgan.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(TicketSerializer(ticket).data)


class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return get_tickets_queryset().filter(buyer=user, is_sold=True).order_by('-purchased_at')



class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)    
    
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


class UserGetMe(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return User.objects.filter(id = user.id)
        else:
            return User.objects.none()
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
        

from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import generics , filters  
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend





class SportView(generics.CreateAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class SportDeleteView(generics.DestroyAPIView):
    queryset = Sport.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


class ClubView(generics.CreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    
    clubs = Club.objects.select_related('sport').all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields ={
        'club_name': ['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith'], # iexact kotta yoki kickina xarflaga qaramasdan qidirish ucun , contains ichda borligini tekshiradi masalan FC bolgan klublar, endwith belgilangan soz bilan tugasa qoshib qidiradi , startswith bu kiritgan soz bilan boshlansa 
        'event_date':['year','month','day'] # date faqat shu sanadagi oyinlar , yillar , oylar, sanasi boyicha qidiradi
    }
    search_fileds = ['club_name'] #clubning nomlari boyicha qidiradi 
    ordering_fields = ['club_name', 'created_at']  # foydalanuvchi faqatshu fieldlar boyicah tartiblat oladi 
    ordering = ['club_name','created_at'] #agar foydalanuvchi tartiblamasa default xolartda tartiblaydi 


class ClubUpdateView(generics.UpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    
class ClubDeleteView(generics.DestroyAPIView):
    queryset = Club.objects.all()
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

    

class ConsertView(generics.CreateAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConsertSerializer


class ConsertListView(generics.ListAPIView):
    queryset = Concert.objects.all()
    serializer_class =  ConsertSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields ={
        'concert_name' :['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith']      
    }
    search_fields = ['concert_name']
    ordering_fields = ['concert_name','created_at']
    ordering = ['concert_name','created_at']

class ConsertUpdateView(generics.UpdateAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConsertSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
      
class ConsertDeleteView(generics.DestroyAPIView):
    queryset = Concert.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


class SingerView(generics.CreateAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer

class SingerListView(generics.ListAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    singers = Singer.objects.select_related('consert').all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields ={
        'singer_name':['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith'],
        'event_date' :['year','month','day']
    }
    search_fileds = ['singer_name']
    ordering_fields = ['singer_name','created_at']
    ordering = ['singer_name','created_at']

class SingerUpdateView(generics.UpdateAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class SingerDeleteView(generics.DestroyAPIView):
    queryset = Singer.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CityView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_field = {
        'city_name': ['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith']
    }
    search_fields = ['city_name']
    ordering_fields =['city_name','created_at']
    ordering =['city_name','created_at']


class CityUpdateView(generics.UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class CityDeleteView(generics.DestroyAPIView):
    queryset = City.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


    

class PlaceView(generics.CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class PlaceListView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    places = Place.objects.select_related('city').all() #select_related bu berilgan modelsni ichida foreign key qb ulangan modellar bilan malumotlani birga ob keladi, ForeigKey bilan OneToOnefield uchun ishilidi 

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields ={
        'place_name':['exact','iexact','contains','icontains','endswith','iendswith','startswith','istartswith']
    }
    search_fields = ['place_name']
    ordering_fields = ['place_name','created_at']
    ordering = ['place_name','created_at']

class PlaceUpdateView(generics.UpdateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class PlaceDeleteView(generics.DestroyAPIView):
    queryset = Place.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


class TicketView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketListView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class TicketDeleteView(generics.DestroyAPIView):
    queryset =Ticket.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)    
    
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

from rest_framework.response import Response


class UserGetMe(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user

        print(user)

        if user.is_authenticated:
            return User.objects.filter(id = user.id)
        else:
            return User.objects.none()
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
        


class CartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartListView(generics.ListAPIView):
    queryset =Cart.objects.all()
    serializer_class = CartSerializer

class CartUpdateView(generics.UpdateAPIView):
    queryset =Cart.objects.all()
    serializer_class = CartSerializer


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)    


class CartDeleteView(generics.DestroyAPIView):
    queryset = Cart.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class CartItemView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartItemListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)    

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class SeatView(generics.CreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class SeatListView(generics.ListAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class SeatUpdateView(generics.UpdateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)    
    
class SeatDeleteView(generics.DestroyAPIView):
    queryset = Seat.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

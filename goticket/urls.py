from django.urls import path ,include
from .views import *
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView





urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('sport/post',SportView.as_view(), name = 'Sport_post'),
    path('sport/get',SportListView.as_view(), name ='Sport_get'),
    path('sport/update/<int:pk>',SportUpdateView.as_view(), name = 'Sport_update'),
    path('sport/delete/<int:pk>',SportDeleteView.as_view(), name='sport_delete'),

    path('club/post', ClubView.as_view(), name = 'Club_post'),
    path('club/get',ClubListView.as_view(), name ='club_get'),
    path('club/update/<int:pk>',ClubUpdateView.as_view(), name = 'club_update'),
    path('club/delete/<int:pk>',ClubDeleteView.as_view(),name = 'club_delete'),

    path('consert/post',ConsertView.as_view(), name = 'consert_post'),
    path('consert/get', ConsertListView.as_view(), name = 'consert_get'),
    path('consert/update/<int:pk>', ConsertUpdateView.as_view(), name = 'consert_update'),
    path('consert/delete/<int:pk>', ConsertDeleteView.as_view(), name = 'consert_delete'),

    path('singer/post', SingerView.as_view(), name = 'singer_post'),
    path('singer/get',SingerListView.as_view(), name = 'singer_get'),
    path('singer/update/<int:pk>', SingerUpdateView.as_view(), name = 'singer_update'),
    path('singer/delete/<int:pk>', SingerDeleteView.as_view(), name = 'singer_delete'),

    path('city/post',CityView.as_view(), name = 'city_post'),
    path('city/get', CityListView.as_view(), name ='city_get'),
    path('city/update/<int:pk>', CityUpdateView.as_view(), name ='city_update'),
    path('city/delete/<int:pk>', CityDeleteView.as_view(), name ='city_delete'),

    path('place/post', PlaceView.as_view(), name = 'place_post'),
    path('place/get', PlaceListView.as_view(), name = 'place_get'),
    path('place/update/<int:pk>',PlaceUpdateView.as_view(), name ='place_update'),
    path('place/delete/<int:pk>',PlaceDeleteView.as_view(), name = 'place_delete'),

    path('ticket/post', TicketView.as_view(), name = 'ticket_post'),
    path('ticket/get', TicketListView.as_view(), name = 'ticket_get'),
    path('ticket/my', MyTicketsView.as_view(), name = 'ticket_my'),
    path('ticket/seats', TicketSeatsView.as_view(), name = 'ticket_seats'),
    path('ticket/seats/<int:section_id>', SectionSeatsView.as_view(), name = 'ticket_section_seats'),
    path('ticket/buy-seat', TicketBuySeatView.as_view(), name = 'ticket_buy_seat'),
    path('ticket/buy/<int:pk>', TicketBuyView.as_view(), name = 'ticket_buy'),
    path('ticket/update/<int:pk>', TicketUpdateView.as_view(), name = 'ticket_update'),
    path('ticket/delete/<int:pk>', TicketDeleteView.as_view(), name = 'ticket_delete'),

    path('user/create', UserCreateView.as_view(), name = 'user_create'),
    path('user/get',UserListView.as_view(), name = 'user_get'),
    path('user/update/<int:pk>', UserUpdateView.as_view(), name = 'user_upadte'),
    path('user/delete/<int:pk>', UserDeleteView.as_view(), name = 'user_delete'),

    path('user/get-me', UserGetMe.as_view(), name='get-me'),
]


# <int:pk> bu bizga aniq obyekti olish ucun ishlatamiz masalan: http://127.0.0.1:8000/api/sport/update/1/ bu 1 id li obyektni olish ucun ishlatamiz
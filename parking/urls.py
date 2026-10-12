from django.urls import path
from parking.views import *
urlpatterns=[path('',home,name='home'),
             path('register/',register_vehicle,name='register_vehicle'),
             path('vehicles/',vehicle_list,name='vehicle_list'),
             path('exit/',vehicle_exit,name='vehicle_exit'),
             path('register-user/',register_user,name='register_user'),
             path('login/',user_login,name='login'),
             path('logout/',user_logout,name='logout'),
             path('dashboard/',user_dashboard,name='user_dashboard'),
             path('ajax-vehicle-search/',ajax_vehicle_search,name='ajax_vehicle_search'),
              ]
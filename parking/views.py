from django.shortcuts import render,redirect
from django.contrib import messages
from parking.models import *
from parking.forms import *
from django.utils import timezone
import math
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum,Avg,Max,Min,Q,F
from django.http import JsonResponse
# Create your views here.
@login_required
def home(request):
    slots=ParkingSlot.objects.all()
    total_slots=slots.count()
    occupied_slots=slots.filter(is_occupied=True).count()
    available_slots=slots.filter(is_occupied=False).count()
    context={
        'slots':slots,
        'total_slots':total_slots,
        'occupied_slots':occupied_slots,
        'available_slots':available_slots
    }
    return render(request,'parking/home.html',context)

@login_required
def register_vehicle(request):
          if request.method=='POST':  
            form=VehicleForm(request.POST)
            if form.is_valid():
                avilable_slot=ParkingSlot.objects.filter(is_occupied=False).first()
                if avilable_slot:
                     vehicle=form.save(commit=False)
                     vehicle.user=request.user
                     vehicle.save()
                     avilable_slot.is_occupied=True
                     avilable_slot.save()
                     ParkingRecord.objects.create(vehicle=vehicle,slot=avilable_slot)
                     messages.success(request,f'vehicle registerd successfully'f'slot{avilable_slot.slot_number}assigned')
                else:
                     messages.error(request,'No parking slots are available')
                return redirect('register_vehicle')
          else:
             form=VehicleForm()
          return render(request,'parking/register_vehicle.html',{'form':form})

@login_required
def vehicle_exit(request):
     if request.method=='POST':
          vehicle_number=request.POST.get('vehicle_number')
          record=ParkingRecord.objects.filter(vehicle__vehicle_number=vehicle_number,vehicle__user=request.user,exit_time__isnull=True).first()
          if record:
            record.exit_time=timezone.now()
            record.save()
            duration=record.exit_time-record.entry_time
            hours=math.ceil(duration.total_seconds()/3600)
            if hours<=1:
                 parking_fee=20
            else:
                 parking_fee=20+(hours-1)*10
            record.parking_fee=parking_fee
            record.save()
            record.slot.is_occupied=False
            record.slot.save()
            receipt={'vehicle_number':record.vehicle.vehicle_number,'slot_number':record.slot.slot_number,'entry_time':record.entry_time,'exit_time':record.exit_time,'duration':duration,'parking_fee':parking_fee,}
            return render(request,'parking/receipt.html',{'receipt':receipt})
            messages.success(request,f'vehicle exited successfully!'f'parking duration{duration}.'f'parkig fee:{parking_fee}')
          else:
               messages.error(request,'No active parking record found for this vehicle')
          return redirect('vehicle_exit')
     return render(request,'parking/vehicle_exit.html')

def register_user(request):
     if request.method=='POST':
          form=UserRegisterForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request,'Account Created Successfully')
               return redirect('login')
     else:
        form=UserRegisterForm()
     return render(request,'parking/register_user.html',{'form':form}) 

def user_login(request):
     if request.method=='POST':
          username=request.POST.get('username')
          password=request.POST.get('password')
          user=authenticate(request,username=username,password=password)
          if user is not None:
               auth_login(request,user)
               messages.success(request,'Login successful')
               return redirect('user_dashboard')
          else:
               messages.error(request,'Invalid username or password')
     return render(request,'parking/login.html') 

def user_logout(request):
     logout(request)
     messages.success(request,'Logged out successfully')
     return redirect('login')

@login_required
def vehicle_list(request):
     search=request.GET.get('search','')
     vehicle_type=request.GET.get('vehicle_type','')
     vehicles=Vehicle.objects.filter(user=request.user,vehicle_number__icontains=search,vehicle_type__icontains=vehicle_type)
     vehicle_types=Vehicle.objects.filter(user=request.user).values_list('vehicle_type',flat=True).distinct()
     return render(request,'parking/vehicle_list.html',{'vehicles':vehicles,'search':search,'vehicle_type':vehicle_type,'vehicle_types':vehicle_types})

@login_required
def user_dashboard(request):
     search=request.GET.get('search','')
     vehicles=Vehicle.objects.filter(user=request.user).annotate(visit_count=Count('parkingrecord'))
     non_bike_vehicles=Vehicle.objects.filter(user=request.user).exclude(vehicle_type='Bike').annotate(visit_count=Count('parkingrecord'))
     real_non_bike_vehicles=Vehicle.objects.filter(user=request.user).exclude(vehicle_type='Bike').exclude(vehicle_number__icontains='TEST')
     parking_records=ParkingRecord.objects.select_related('vehicle','slot').filter(vehicle__user=request.user,
     vehicle__vehicle_number__icontains=search).order_by('-entry_time')
     long_parking_records=ParkingRecord.objects.filter(vehicle__user=request.user,exit_time__gt=F('entry_time'))
     car_parking_records=ParkingRecord.objects.filter(vehicle__user=request.user,vehicle__vehicle_type='Car')
     total_visits=parking_records.count()
     fee_stats=parking_records.aggregate(total=Sum('parking_fee'),average=Avg('parking_fee'),highest=Max('parking_fee'),lowest=Min('parking_fee'))
     total_revenue=fee_stats['total'] or 0
     average_fee=fee_stats['average'] or 0
     highest_fee=fee_stats['highest'] or 0
     lowest_fee=fee_stats['lowest'] or 0
     car_or_bike_vehicles=Vehicle.objects.filter(Q(user=request.user) & (Q(vehicle_type='Car')|Q(vehicle_type='Bike')))
     vehicle_data=Vehicle.objects.filter(user=request.user).values('vehicle_number','vehicle_type')
     vehicle_numbers=Vehicle.objects.filter(user=request.user).values_list('vehicle_number',flat=True)
     
     return render(request,'parking/user_dashboard.html',{'vehicles':vehicles,'parking_records':parking_records,'search':search,'non_bike_vehicles':non_bike_vehicles,'total_visits':total_visits,'total_revenue':total_revenue,'average_fee':average_fee,'highest_fee':highest_fee,'lowest_fee':lowest_fee,'car_or_bike_vehicles':car_or_bike_vehicles,'real_non_bike_vehicles':real_non_bike_vehicles,'car_parking_records':car_parking_records,'long_parking_records':long_parking_records,'vehicle_data':vehicle_data,'vehicle_numbers':vehicle_numbers})

@login_required
def ajax_vehicle_search(request):
     search=request.GET.get('search','').strip()
     vehicles=Vehicle.objects.filter(user=request.user,vehicle_number__icontains=search).order_by('vehicle_number')
     data=[]
     for vehicle in vehicles:
          data.append({'vehicle_number':vehicle.vehicle_number,'vehicle_type':vehicle.vehicle_type})
     return JsonResponse({'vehicles':data})
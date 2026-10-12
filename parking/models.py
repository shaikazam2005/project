from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ParkingSlot(models.Model):
    slot_number=models.CharField(max_length=10,unique=True)
    is_occupied=models.BooleanField(default=False)
    def __str__(self):
        return self.slot_number


class Vehicle(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    vehicle_number=models.CharField(max_length=20,unique=True)
    vehicle_type=models.CharField(max_length=20)
    def __str__(self):
        return self.vehicle_number


class ParkingRecord(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    slot=models.ForeignKey(ParkingSlot,on_delete=models.CASCADE)
    entry_time=models.DateTimeField(auto_now_add=True)
    exit_time=models.DateTimeField(null=True,blank=True)
    parking_fee=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    def __str__(self):
        return f"{self.vehicle.vehicle_number}-{self.slot.slot_number}"


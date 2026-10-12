from django.contrib import admin
from parking.models import ParkingSlot,ParkingRecord,Vehicle
# Register your models here.

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display=('slot_number','is_occupied')
    list_filter=('is_occupied',)
    search_fields=('slot_number',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display=('vehicle_number','vehicle_type','user')
    list_filter=('vehicle_type',)
    search_fields=('vehicle_number','user__username')


@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    list_display=('vehicle','slot','entry_time','exit_time','parking_fee')
    list_filter=('entry_time','exit_time')
    search_fields=('vehicle__vehicle_number','slot__slot_number')
    ordering=('-entry_time',)

from django import forms
from parking.models import Vehicle
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VehicleForm(forms.ModelForm):
    class Meta:
        model=Vehicle
        fields=['vehicle_number','vehicle_type']
    def clean_vehicle_number(self):
        vehicle_number=self.cleaned_data.get('vehicle_number','').strip().upper()
        if not vehicle_number:
            raise forms.ValidationError('Vehicle number is required.')
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            raise forms.ValidationError('This vehicle number is already registered')
        return vehicle_number
    
class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
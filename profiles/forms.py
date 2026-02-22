from django import forms
from .models import Profile, MoverProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'location']


class MoverProfileForm(forms.ModelForm):
    class Meta:
        model = MoverProfile
        fields = [
            'truck_size',
            'service_area',
            'price_range',
            'availability'
        ]
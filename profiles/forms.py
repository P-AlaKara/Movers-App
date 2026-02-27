from django import forms
from .models import Profile, MoverProfile

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs.update({'class': (existing + ' input').strip()})
            if 'placeholder' not in f.widget.attrs:
                f.widget.attrs['placeholder'] = f.label

    class Meta:
        model = Profile
        fields = ['phone_number', 'location']


class MoverProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs.update({'class': (existing + ' input').strip()})
            if 'placeholder' not in f.widget.attrs:
                f.widget.attrs['placeholder'] = f.label

    class Meta:
        model = MoverProfile
        fields = [
            'truck_size',
            'service_area',
            'price_range',
            'availability'
        ]
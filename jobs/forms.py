from django import forms
from .models import MovingRequest


class MovingRequestForm(forms.ModelForm):
    class Meta:
        model = MovingRequest
        fields = [
            "pickup_location",
            "dropoff_location",
            "moving_date",
            "item_description",
            "budget",
        ]
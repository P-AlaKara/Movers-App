from django import forms
from .models import MovingRequest, Bid


class MovingRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["moving_date"].input_formats = ["%Y-%m-%d"]
        
    class Meta:
        model = MovingRequest
        fields = [
            "pickup_location",
            "dropoff_location",
            "moving_date",
            "item_description",
            "budget",
        ]
        widgets = {
            "moving_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'message']
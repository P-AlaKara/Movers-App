from django import forms
from .models import MovingRequest, Bid


class MovingRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ensure date input accepts iso format
        self.fields["moving_date"].input_formats = ["%Y-%m-%d"]
        # add Bulma input class to every field widget
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs.update({'class': (existing + ' input').strip()})
            if 'placeholder' not in f.widget.attrs:
                f.widget.attrs['placeholder'] = f.label
        
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs.update({'class': (existing + ' input').strip()})
            if 'placeholder' not in f.widget.attrs:
                f.widget.attrs['placeholder'] = f.label

    class Meta:
        model = Bid
        fields = ['price', 'message']
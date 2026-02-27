from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('mover', 'Mover'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs.update({'class': (existing + ' input').strip()})
            if 'placeholder' not in f.widget.attrs:
                f.widget.attrs['placeholder'] = f.label

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    '''def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user'''
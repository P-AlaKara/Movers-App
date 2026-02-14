from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('mover', 'Mover'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class MoverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    truck_size = models.CharField(max_length=100, blank=True)
    service_area = models.CharField(max_length=255, blank=True)
    price_range = models.CharField(max_length=100, blank=True)
    availability = models.BooleanField(default=True)
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Mover: {self.user.username}"
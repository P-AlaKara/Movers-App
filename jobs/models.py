from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MovingRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    moving_date = models.DateField()
    item_description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id} by {self.customer.username}"
    
class JobAssignment(models.Model):
    moving_request = models.OneToOneField(MovingRequest, on_delete=models.CASCADE)
    mover = models.ForeignKey(User, on_delete=models.CASCADE)
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('assigned', 'Assigned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ),
        default='assigned'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job #{self.moving_request.id} assigned to {self.mover.username} ({self.status})"
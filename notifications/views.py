from django.shortcuts import render, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()

    return render(request, "notifications/notifications.html", {
        "notifications": notifications
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")
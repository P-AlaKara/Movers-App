from .models import Notification

def create_notification(user, message, link=None):
    Notification.objects.create(
        user=user,
        message=message,
        link=link
    )
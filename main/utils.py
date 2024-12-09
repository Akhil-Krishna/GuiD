from .models import Notification

def notify_user(user, message, link=None):
    Notification.objects.create(user=user, message=message, link=link)
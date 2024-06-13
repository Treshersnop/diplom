from core import models


def create_notification(title: str, target_id: int, text: str = ''):
    return models.Notification.objects.create(
        title=title,
        text=text,
        target_id=target_id,
    )


def get_notification_data(notification: models.Notification):
    return {
        'title': notification.title,
        'text': notification.text,
        'target_id': notification.target_id,
        'is_watched': False,
    }

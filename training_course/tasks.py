from io import BytesIO

from celery import shared_task
from django.db import transaction
from webpush import send_user_notification

import core.datatools
from core.models import User
from training_course import datatools, models


@shared_task
def create_test(test_file_name: str, test_file: bytes, lesson_id: int, user_id: int) -> None:
    test = models.Test(lesson_id=lesson_id)
    test_file = BytesIO(test_file)

    try:
        questions, answers = (
            datatools.parse_docx_test(test_file, test)
            if test_file_name.endswith('docx')
            else (datatools.parse_excel_test(test_file, test))
        )

        with transaction.atomic():
            test.save()
            models.Question.objects.bulk_create(questions)
            models.Answer.objects.bulk_create(answers)

        notification = core.datatools.create_notification(
            title=f'Тест к уроку {test.lesson.name} успешно загрузился!', target_id=user_id
        )
        notification_data = core.datatools.get_notification_data(notification)
        send_notification.delay(notification_data)

    except Exception as e:
        notification = core.datatools.create_notification(
            title=f'Тест к уроку {test.lesson.name} не загрузился!',
            text='Пожалуйста, проверьте правильность данных!',
            target_id=user_id,
        )
        notification_data = core.datatools.get_notification_data(notification)
        send_notification.delay(notification_data)

        administrator = User.objects.filter(is_superuser=True).only('id').first()
        core.datatools.create_notification(title='Ошибка в загрузке файла', text=e.args[0], target_id=administrator.id)


@shared_task
def send_notification(notification_data: dict) -> None:
    """Отправка уведомлений"""
    notify_user = User.objects.filter(id=notification_data['target_id']).first()
    if notify_user:
        send_user_notification(
            user=notify_user, payload={'head': notification_data['title'], 'body': notification_data['text']}, ttl=1000
        )

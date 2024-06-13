from io import BytesIO

from celery import shared_task
from django.db import transaction
from pywebpush import webpush, WebPushException

from core.datatools import create_notification
from training_course import datatools, models


# @shared_task
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
            notification = create_notification(title='Тест успешно загрузился!', target_id=user_id)
            # return notification

    except Exception as e:
        print(5)


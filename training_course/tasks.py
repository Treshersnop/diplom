from io import BytesIO

from celery import shared_task
from django.db import transaction

from training_course import datatools, models


@shared_task
def create_test(test_file_name: str, test_file: bytes, lesson_id: int) -> None:
    test = models.Test(lesson_id=lesson_id)
    # try:
    #     questions, answers = parse_docx_test(test_file, test) if test_file.name.endswith('docx') else (
    #         parse_excel_test(test_file, test)
    #     )
    #
    #     models.Question.objects.bulk_create(questions)
    #     models.Answer.objects.bulk_create(answers)
    # except:
    #     print(5)
    test_file = BytesIO(test_file)
    questions, answers = (
        datatools.parse_docx_test(test_file, test)
        if test_file_name.endswith('docx')
        else (datatools.parse_excel_test(test_file, test))
    )
    with transaction.atomic():
        test.save()
        models.Question.objects.bulk_create(questions)
        models.Answer.objects.bulk_create(answers)

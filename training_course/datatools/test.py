import io
from math import isnan

import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from docx import Document

from training_course import models


def create_test(test_file: InMemoryUploadedFile, lesson: models.Lesson) -> None:
    test = models.Test.objects.create(lesson=lesson)
    # try:
    #     questions, answers = parse_docx_test(test_file, test) if test_file.name.endswith('docx') else (
    #         parse_excel_test(test_file, test)
    #     )
    #
    #     models.Question.objects.bulk_create(questions)
    #     models.Answer.objects.bulk_create(answers)
    # except:
    #     print(5)
    questions, answers = (
        parse_docx_test(test_file, test) if test_file.name.endswith('docx') else (parse_excel_test(test_file, test))
    )

    models.Question.objects.bulk_create(questions)
    models.Answer.objects.bulk_create(answers)


def parse_docx_test(test_file: InMemoryUploadedFile, test: models.Test) -> (list[models.Question], list[models.Answer]):
    test_file = io.BytesIO(test_file.read())
    document = Document(test_file)
    pars = document.paragraphs
    questions = []
    answers = []
    for par in pars:
        string_data = par.text
        # если строка содержит заголовок "вопрос", то будет считаться вопросом
        if string_data.lower().startswith('вопрос'):
            question = models.Question(test=test, name=string_data.split('.', maxsplit=1)[-1])
            questions.append(question)
        # В другом случае это будет ответом.
        # Правильным будет считаться ответ, который либо выделен жирным, либо выделен цветом, отличного от черного.
        else:
            answer_data = par.runs[0]
            answer = models.Answer(question=questions[-1], name=string_data.split(')', maxsplit=1)[-1])
            if answer_data.font.bold or answer_data.font.color.rgb:
                answer.is_right = True

            answers.append(answer)

    return questions, answers


def parse_excel_test(
    test_file: InMemoryUploadedFile, test: models.Test
) -> (list[models.Question], list[models.Answer]):
    test_file = io.BytesIO(test_file.read())
    document = pd.read_excel(test_file, header=None)
    strings_data = document.values.tolist()
    questions = []
    answers = []
    for string_data in strings_data:
        question_name = string_data[0]
        # в строке вопросом будет являться первый столбец, который является не пустым
        is_question = not (question_name == '' or isinstance(question_name, float) and isnan(question_name))
        if is_question:
            question = models.Question(test=test, name=question_name)
            questions.append(question)

        answer_name = string_data[2]
        # ответ будет считаться правильным, если третий столбец не равен пустой строке или не равен 0
        answer_is_right = not (
            answer_name == 0
            or answer_name == '0'
            or answer_name == ''
            or (isinstance(answer_name, float) and isnan(answer_name))
        )
        # если ответом будет цифра, чтобы вместо 1.0 возвращалось 1
        if isinstance(answer_name, float) and answer_name.is_integer():
            answer_name = int(answer_name)
        answer = models.Answer(question=questions[-1], name=answer_name)
        if answer_is_right:
            answer.is_right = True

        answers.append(answer)

    return questions, answers

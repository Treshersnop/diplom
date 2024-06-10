import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from docx import Document

from training_course import models


def create_test(test_file: InMemoryUploadedFile, lesson: models.Lesson):
    test = models.Test.objects.create(lesson=lesson)
    try:
        questions, answers = parse_docx_test(test_file, test) if test_file.name.endswith('docx') else (
            parse_excel_test(test_file, test)
        )

        models.Question.objects.bulk_create(questions)
        models.Answer.objects.bulk_create(answers)
    except:
        print(5)


def parse_docx_test(
        test_file: InMemoryUploadedFile,
        test: models.Test
) -> (list[models.Question], list[models.Answer], bool):
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
            answer = models.Answer(
                question=questions[-1],
                name=string_data.split(')', maxsplit=1)[-1],
                is_right=True
            ) if answer_data.font.bold or answer_data.font.color.rgb else (
                models.Answer(question=questions[-1], name=string_data.split(')', maxsplit=1)[-1])
            )

            answers.append(answer)

    return questions, answers, True


def parse_excel_test(test_file: InMemoryUploadedFile, test: models.Test):
    print(5)
    return [], [], True

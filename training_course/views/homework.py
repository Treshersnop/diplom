from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect

from training_course import models


@login_required
def create_homework(request: WSGIRequest, pk: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        lesson = models.Lesson.objects.get(id=pk)
        homework = models.Homework.objects.create(
            learner_id=request.user.id,
            task=lesson.task,
            description='123'
        )
        if files := request.files.getlist('files'):
            for file in files:
                homework.files.create(file=file, name=file.name)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

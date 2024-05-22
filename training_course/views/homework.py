from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from training_course import models, forms


class HomeworkCreate(LoginRequiredMixin, CreateView):
    form_class = forms.CreateHomework
    template_name = 'homework/homework_create.html'

    def get(self, request: WSGIRequest, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(
                lessons__task__id=kwargs['pk'],
                subscriptions__user_id=current_user.id,
        ).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        homework = form.save(commit=False)

        user = self.request.user
        homework.learner_id = user.id
        task_id = self.kwargs['pk']
        homework.task_id = task_id
        homework.save()

        if files := form.files.getlist('files'):
            for file in files:
                homework.files.create(file=file, name=file.name)

        return HttpResponseRedirect(reverse('training_course:lesson_detail', kwargs={'pk': homework.task.lesson.id}))


class HomeworkUpdate(LoginRequiredMixin, UpdateView):
    model = models.Homework
    template_name = 'homework/homework_update.html'
    form_class = forms.UpdateHomework
    context_object_name = 'homework'

    def get(self, request: WSGIRequest, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.Homework.objects.filter(learner__id=current_user.id).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        homework = form.save(commit=False)

        if files := form.files.getlist('files'):
            for file in files:
                homework.files.create(file=file, name=file.name)

        return HttpResponseRedirect(reverse('training_course:lesson_detail', kwargs={'pk': homework.task.lesson.id}))

    def get_success_url(self) -> str:
        return reverse('training_course:lesson_detail', kwargs={'pk': self.object.task.lesson.id})


@login_required
def check_homework(request: WSGIRequest, pk: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        hw = models.Homework.objects.get(id=pk)
        hw.is_checked = True
        hw.save(update_fields=['is_checked'])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

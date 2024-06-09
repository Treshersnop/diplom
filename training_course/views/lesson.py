from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView

from training_course import datatools, models, forms


class LessonDetail(LoginRequiredMixin, DetailView):
    model = models.Lesson
    template_name = 'lesson/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)

        lesson = kwargs['object']

        try:
            task = lesson.task

            current_user_id = self.request.user.id
            if not models.TrainingCourse.objects.filter(
                    lessons__id=lesson.id, responsible__id=current_user_id
            ).exists():
                context['user_homework'] = task.homeworks.filter(learner_id=current_user_id).first()
                return context

            context['homeworks'] = task.homeworks.order_by('is_checked')
        except ObjectDoesNotExist:
            context['user_homework'] = None
        return context

    def get(self, request: WSGIRequest, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(
                Q(lessons__id=kwargs['pk']) &
                (Q(responsible__id=current_user.id) | Q(subscriptions__user__id=current_user.id))
        ).exists():
            return super().get(request, *args, **kwargs)

        raise Http404


class LessonCreate(LoginRequiredMixin, CreateView):
    form_class = forms.CreateLesson
    template_name = 'lesson/lesson_create.html'

    def get(self, request: WSGIRequest, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(
                id=kwargs['pk'],
                responsible__id=current_user.id
        ).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        lesson = form.save(commit=False)
        lesson.course_id = self.kwargs['pk']
        lesson.save()

        if files := form.files.getlist('files'):
            for file in files:
                lesson.files.create(file=file, name=file.name)

        if form.cleaned_data.get('task_name'):
            task = models.Task.objects.create(
                name=form.cleaned_data['task_name'],
                description=form.cleaned_data['task_description'],
                lesson=lesson,
            )

            if task_files := form.files.getlist('task_files'):
                for file in task_files:
                    task.files.create(file=file, name=file.name)

        if test_file := form.files.getlist('test_file'):
            datatools.test.create_test(test_file[0], lesson)

        return HttpResponseRedirect(reverse('training_course:lesson_detail', kwargs={'pk': lesson.id}))


class LessonUpdate(LoginRequiredMixin, UpdateView):
    model = models.Lesson
    template_name = 'lesson/lesson_update.html'
    form_class = forms.UpdateLesson
    context_object_name = 'lesson'

    def get(self, request: WSGIRequest, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(
                lessons__id=kwargs['pk'],
                responsible__id=current_user.id
        ).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        lesson = form.save(commit=False)

        if files := form.files.getlist('files'):
            for file in files:
                lesson.files.create(file=file, name=file.name)

        if form.cleaned_data.get('task_name'):
            try:
                task = lesson.task
                task.name = form.cleaned_data['task_name']
                task.description = form.cleaned_data['task_description']
                task.save()
            except ObjectDoesNotExist:
                task = models.Task.objects.create(
                    name=form.cleaned_data['task_name'],
                    description=form.cleaned_data['task_description'],
                    lesson=lesson,
                )

            if task_files := form.files.getlist('task_files'):
                for file in task_files:
                    task.files.create(file=file, name=file.name)

        return HttpResponseRedirect(reverse('training_course:lesson_detail', kwargs={'pk': lesson.id}))

    def get_success_url(self) -> str:
        return reverse('training_course:lesson_detail', kwargs={'pk': self.object.pk})

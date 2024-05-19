from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView
from requests import Request

from training_course import models, forms


class LessonDetail(LoginRequiredMixin, DetailView):
    model = models.Lesson
    template_name = 'lesson/lesson_detail.html'
    context_object_name = 'lesson'

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(
                lessons__id=kwargs['pk'], subscriptions__user__id=current_user.id
        ).exists():
            return super().get(request, *args, **kwargs)

        raise Http404


class LessonCreate(LoginRequiredMixin, CreateView):
    form_class = forms.CreateLesson
    template_name = 'lesson/lesson_create.html'

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        course = form.save()
        course.responsible.add(self.request.user.id)
        return HttpResponseRedirect(reverse('training_course:course_detail', kwargs={'pk': course.id}))


class LessonUpdate(LoginRequiredMixin, UpdateView):
    model = models.Lesson
    template_name = 'lesson/lesson_update.html'
    form_class = forms.UpdateCourse
    context_object_name = 'course'

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(id=kwargs['pk'], responsible__id=current_user.id).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def get_success_url(self) -> str:
        return reverse('training_course:course_detail', kwargs={'pk': self.object.pk})
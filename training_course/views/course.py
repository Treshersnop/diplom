from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from requests import Request

from training_course import models, filters, forms


class CourseList(ListView):
    queryset = models.TrainingCourse
    template_name = 'course/course_list.html'
    context_object_name = 'course_list'

    def get_filters(self) -> filters:
        return filters.Course(self.request.GET, request=self.request)

    def get_context_data(self, *, object_list: Any = None, **kwargs: dict) -> dict:
        context = super().get_context_data(object_list=None, **kwargs)
        context['filter'] = self.get_filters()
        return context

    def get_queryset(self) -> QuerySet:
        courses = self.get_filters().qs
        return courses.filter((Q(to_data__gte=now().date()) | Q(to_data=None)), is_active=True).order_by('id')


class CourseDetail(DetailView):
    model = models.TrainingCourse
    template_name = 'course/course_detail.html'
    context_object_name = 'course'


class CourseCreate(LoginRequiredMixin, CreateView):
    form_class = forms.CreateCourse
    template_name = 'course/course_create.html'

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        course = form.save()
        course.responsible.add(self.request.user.id)
        return HttpResponseRedirect(reverse('training_course:course_detail', kwargs={'pk': course.id}))


class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = models.TrainingCourse
    template_name = 'course/course_update.html'
    form_class = forms.UpdateCourse
    context_object_name = 'course'

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(id=kwargs['pk'], responsible__id=current_user.id).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def get_success_url(self) -> str:
        return reverse('training_course:course_detail', kwargs={'pk': self.object.pk})

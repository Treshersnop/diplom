from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.request import Request

from training_course import models, filters, forms


class CourseList(ListView):
    queryset = models.TrainingCourse.objects.all()
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

    def get_context_data(self, *, object_list: Any = None, **kwargs: dict) -> dict:
        context = super().get_context_data(object_list=None, **kwargs)
        course = self.get_object()
        user = self.request.user
        context['has_edit'] = course.responsible.filter(id=user.id).exists()
        return context

class CourseCreate(LoginRequiredMixin, CreateView):
    form_class = forms.CreateCourse
    template_name = 'course/course_create.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('training_course:course_list')

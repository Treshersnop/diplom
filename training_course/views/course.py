from datetime import timedelta
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q, Count, F
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

    def get(self, request: Request, *args: Any, **kwargs: Any):
        response = super().get(request, *args, **kwargs)
        # увеличивает количество просмотров на 1 если пользователь не является его создателем
        current_user = self.request.user
        if not self.object.responsible.filter(id=current_user.id).exists():
            self.object.number_of_clicks += 1
            self.object.save(update_fields=['number_of_clicks'])

        return response


class CourseCreate(LoginRequiredMixin, CreateView):
    form_class = forms.CreateCourse
    template_name = 'course/course_create.html'

    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse | Http404:
        current_user = self.request.user

        if current_user.is_staff:
            return super().get(request, *args, **kwargs)

        raise Http404

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


class CourseStatistic(DetailView):
    model = models.TrainingCourse
    template_name = 'course/course_statistic.html'
    context_object_name = 'course'

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if models.TrainingCourse.objects.filter(id=kwargs['pk'], responsible__id=current_user.id).exists():
            return super().get(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        course = self.object
        subscription_statistic = course.subscriptions.filter(dc__lte=now(), dc__gte=now() - timedelta(days=7)).count()

        lesson_statistic = course.lessons.annotate(
            count_homeworks=Count('task__homeworks', distinct=True),
            count_not_checked_homeworks=Count(
                'task__homeworks', filter=Q(task__homeworks__is_checked=False), distinct=True
            ),
            count_checked_homeworks=Count(
                'task__homeworks', filter=Q(task__homeworks__is_checked=True), distinct=True
            ),
            not_done_homeworks=Count('course__subscriptions', distinct=True) - F('count_homeworks'),
        )

        context['lessons'] = lesson_statistic
        context['subscription_statistic'] = subscription_statistic

        return context

from typing import Any
from urllib.request import Request

from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView

from core import forms, models
import training_course.models


class Login(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return self.request.GET.get('next') or reverse_lazy('training_course:course_list')

    def form_invalid(self, form: forms) -> HttpResponse:
        messages.error(self.request, 'Неверный логин или пароль.')
        return self.render_to_response(self.get_context_data(form=form))


class Register(FormView):
    form_class = UserCreationForm
    template_name = 'user/authorization.html'
    success_url = reverse_lazy('core:register_profile')

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        form.save()
        user_cache = authenticate(
            self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1']
        )
        auth_login(self.request, user_cache)
        return super().form_valid(form)


class ProfileCreate(LoginRequiredMixin, FormView):
    form_class = forms.CreateProfile
    template_name = 'user/create_profile_auth.html'
    success_url = reverse_lazy('training_course:course_list')

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        user = self.request.user
        user.email = form.cleaned_data.get('email')
        user.is_staff = form.cleaned_data.get('is_staff')
        user.save(update_fields=['email', 'is_staff'])
        form.instance.user = user
        form.save()
        return super().form_valid(form)


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = models.UserProfile
    template_name = 'user/detail_user.html'
    context_object_name = 'profile'
    slug_field = 'user__username'
    slug_url_kwarg = 'user_slug'

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)

        current_user = self.request.user

        context['user_responsible_for_courses'] = (
            training_course.models.TrainingCourse.objects.filter(responsible=current_user).values('id', 'name')
        )
        # выводит название курсов и количество невыполненных заданий в курсе
        context['subscriptions'] = (
            training_course.models.Subscription.objects.filter(
                user=current_user.id, is_blocked=False
            ).annotate(
                count_all_hw=Count('course__lessons__task', distinct=True),
                count_done_hw=Count(
                    'course__lessons__task__homeworks',
                    filter=Q(course__lessons__task__homeworks__learner=current_user),
                    distinct=True
                )
            ).
            values('course__id', 'course__name', 'count_all_hw', 'count_done_hw')
        )

        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = models.UserProfile
    template_name = 'user/update_profile.html'
    form_class = forms.UpdateProfile
    context_object_name = 'profile'
    slug_field = 'user__username'
    slug_url_kwarg = 'user_slug'

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        user = self.request.user
        user.email = form.cleaned_data.get('email')
        user.save(update_fields=['email'])
        form.instance.user = user
        return super().form_valid(form)

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user
        if current_user.username == kwargs.get('user_slug', None):
            return super().get(request, *args, **kwargs)

        raise Http404

    def get_success_url(self) -> str:
        return reverse_lazy('core:profile', kwargs={'user_slug': self.request.user.username})

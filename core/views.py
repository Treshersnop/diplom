from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, DetailView, UpdateView
from rest_framework.request import Request

from core import forms, models


class Login(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return self.request.GET.get('next') or reverse_lazy('training_course:course_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль.')
        return self.render_to_response(self.get_context_data(form=form))


class Register(FormView):
    form_class = UserCreationForm
    template_name = 'user/authorization.html'
    success_url = reverse_lazy('core:register_profile')

    def form_valid(self, form):
        form.save()
        user_cache = authenticate(
            self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1']
        )
        auth_login(self.request, user_cache)
        return super().form_valid(form)


class CreateProfile(LoginRequiredMixin, FormView):
    form_class = forms.CreateProfile
    template_name = 'user/create_profile_auth.html'
    success_url = reverse_lazy('training_course:course_list')

    def form_valid(self, form):
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

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse | Http404:
        current_user = self.request.user

        if current_user.profile.id == kwargs.get('pk', None):
            return super().get(request, *args, **kwargs)

        raise Http404


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = models.UserProfile
    template_name = 'user/update_profile.html'
    form_class = forms.UpdateProfile
    context_object_name = 'profile'

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data.get('email')
        user.save(update_fields=['email'])
        form.instance.user = user
        return super().form_valid(form)

    def get(self, request: Request, *args: list, **kwargs: dict):
        current_user = self.request.user
        if current_user.profile.id == kwargs.get('pk', None):
            return super().get(request, *args, **kwargs)

        raise Http404

    def get_success_url(self) -> str:
        return reverse_lazy('core:profile', kwargs={'pk': self.object.pk})
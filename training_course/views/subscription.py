from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.views import View

from training_course import models


class SubscriptionCreate(LoginRequiredMixin, View):
    def post(self, request: WSGIRequest, pk: int) -> HttpResponseRedirect:
        models.Subscription.objects.create(user_id=request.user.id, course_id=pk)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SubscriptionDelete(LoginRequiredMixin, View):
    def post(self, request: WSGIRequest, pk: int) -> HttpResponseRedirect:
        models.Subscription.objects.filter(user_id=request.user.id, course_id=pk).delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

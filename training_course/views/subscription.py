from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect

from training_course import models


@login_required
def create_subscription(request: WSGIRequest, pk: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        models.Subscription.objects.create(user_id=request.user.id, course_id=pk)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_subscription(request: WSGIRequest, pk: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        models.Subscription.objects.filter(user_id=request.user.id, course_id=pk).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

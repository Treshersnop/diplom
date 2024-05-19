from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from requests import Request

from training_course import models


@login_required
def create_subscription(request: Request, pk: int):
    if request.method == 'POST':
        models.Subscription.objects.create(user_id=request.user.id, course_id=pk)

    return HttpResponseRedirect(reverse('training_course:course_list'))


@login_required
def delete_subscription(request: Request, pk: int):
    if request.method == 'POST':
        models.Subscription.objects.filter(user_id=request.user.id, course_id=pk).delete()

    return HttpResponseRedirect(reverse('training_course:course_list'))
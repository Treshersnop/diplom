from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, ListView

import core.models
from chat import forms, models


@login_required
def create_room(request: WSGIRequest, pk: int) -> HttpResponseRedirect | Http404:
    if request.method == 'POST':
        user = request.user.id

        participant = core.models.User.objects.filter(id=pk).first()
        if not participant:
            raise Http404

        room = models.Room.objects.create()
        room.participants.set([user, participant])

        return HttpResponseRedirect(reverse('chat:room_detail', kwargs={'pk': room.id}))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RoomDetail(LoginRequiredMixin, DetailView):
    model = models.Room
    template_name = 'room/room_detail.html'
    context_object_name = 'room'


class RoomList(ListView):
    template_name = 'room/room_list.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        current_user = self.request.user
        return models.Room.objects.filter(participants__id=current_user.id)


class CreateMessage(LoginRequiredMixin, UpdateView):
    model = models.Message
    form_class = forms.Message

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        message = form.save(commit=False)

        user = self.request.user
        message.sender_id = user.id

        message.room_id = self.kwargs['pk']
        message.save()

        if files := form.files.getlist('files'):
            for file in files:
                message.files.create(file=file, name=file.name)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

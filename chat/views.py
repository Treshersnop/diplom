from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, Subquery, OuterRef
from django.db.models.functions import JSONObject
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView

import core.models
from chat import forms, models


@login_required
def get_room(request: WSGIRequest, pk: int) -> HttpResponseRedirect:
    if request.method == 'GET':
        current_user = request.user
        participant = core.models.User.objects.filter(id=pk).first()
        if not participant:
            raise Http404

        if room := models.Room.objects.filter(
                participants__id=current_user.id
        ).filter(
            participants__id=participant.id
        ).first():
            return HttpResponseRedirect(reverse('chat:room_detail', kwargs={'pk': room.id}))

        room = models.Room.objects.create()
        room.participants.set([current_user.id, participant.id])
        return HttpResponseRedirect(reverse('chat:room_detail', kwargs={'pk': room.id}))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RoomDetail(LoginRequiredMixin, DetailView):
    model = models.Room
    template_name = 'room/room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)

        room = context['room']
        context['messages'] = room.messages.order_by('-dc')

        current_user = self.request.user
        setattr(room, 'name', room.participants.exclude(id=current_user.id).first())

        return context


class RoomList(ListView):
    template_name = 'room/room_list.html'
    context_object_name = 'room_list'

    def get_queryset(self) -> QuerySet:
        current_user = self.request.user
        last_message = models.Message.objects.filter(room=OuterRef('pk')).order_by('-dc').values(
            json=JSONObject(last_dc='dc', text_message='description')
        )

        return models.Room.objects.filter(
            participants__id=current_user.id
        ).annotate(last_message=Subquery(last_message[:1])).order_by('-last_message')

    def get_context_data(self, *, object_list: QuerySet | None = None, **kwargs: Any) -> dict:
        context = super().get_context_data(object_list=None, **kwargs)

        room_list = context['room_list']
        current_user = self.request.user
        for room in room_list:
            setattr(room, 'member', room.participants.exclude(id=current_user.id).first())

        return context


class CreateMessage(LoginRequiredMixin, CreateView):
    model = models.Message
    form_class = forms.Message

    def form_valid(self, form: forms) -> HttpResponseRedirect:
        if not form.cleaned_data['description']:
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        message = form.save(commit=False)

        user = self.request.user
        message.sender_id = user.id

        message.room_id = self.kwargs['pk']
        message.save()

        if files := form.files.getlist('files'):
            for file in files:
                message.files.create(file=file, name=file.name)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

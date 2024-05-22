from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('chat/create/<int:pk>', views.create_room, name='room_create'),

    path('subscription/<int:pk>/create/', views.CreateMessage.as_view(), name='create_message'),
]

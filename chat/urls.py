from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('room/create/<int:pk>/', views.create_room, name='room_create'),

    path('room/list/', views.RoomList.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetail.as_view(), name='room_detail'),

    path('chat/<int:pk>/create/', views.CreateMessage.as_view(), name='message_create'),
]

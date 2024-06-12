from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('room/get/<int:pk>/', views.get_room, name='room_get'),
    path('room/list/', views.RoomList.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetail.as_view(), name='room_detail'),
    path('chat/<int:pk>/create/', views.CreateMessage.as_view(), name='message_create'),
]

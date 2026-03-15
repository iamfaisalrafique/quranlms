from django.urls import path
from apps.chat import views

app_name = 'chat'

urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='room-list'),
    path('room/<int:student_id>/start/', views.StartRoomView.as_view(), name='room-start'),
    path('room/<int:room_id>/messages/', views.MessageHistoryView.as_view(), name='room-messages'),
    path('message/<int:pk>/read/', views.MarkReadView.as_view(), name='message-read'),
]

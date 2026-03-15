from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.chat.models import ChatRoom, ChatMessage
from apps.chat.serializers import ChatRoomSerializer, ChatMessageSerializer
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class RoomListView(generics.ListAPIView):
    """GET /api/chat/rooms/ — list rooms for the current teacher or student."""
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return ChatRoom.objects.filter(teacher=user).select_related('student', 'teacher', 'academy')
        return ChatRoom.objects.filter(student=user).select_related('student', 'teacher', 'academy')


class StartRoomView(APIView):
    """POST /api/chat/room/<student_id>/start/ — teacher creates or gets a room with a student."""
    permission_classes = [IsAuthenticated]

    def post(self, request, student_id):
        if request.user.role != 'teacher':
            return Response({'detail': 'Only teachers can start chat rooms.'}, status=status.HTTP_403_FORBIDDEN)

        student = get_object_or_404(User, pk=student_id, role='student')
        from apps.academy.models import Academy

        # Use teacher's first academy (academy scoping)
        try:
            academy = request.user.teacher_profile.academy
        except Exception:
            return Response({'detail': 'Teacher not linked to an academy.'}, status=status.HTTP_400_BAD_REQUEST)

        room, created = ChatRoom.objects.get_or_create(
            student=student,
            teacher=request.user,
            defaults={'academy': academy},
        )
        serializer = ChatRoomSerializer(room, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class MessageHistoryView(generics.ListAPIView):
    """GET /api/chat/room/<room_id>/messages/ — paginated message history."""
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        user = self.request.user
        room = get_object_or_404(ChatRoom, pk=room_id)

        # only room participants can read
        if user.id not in (room.student_id, room.teacher_id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()

        return ChatMessage.objects.filter(room=room).select_related('sender')


class MarkReadView(APIView):
    """PATCH /api/chat/message/<pk>/read/ — mark a message as read."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        message = get_object_or_404(ChatMessage, pk=pk)
        if request.user.id not in (message.room.student_id, message.room.teacher_id):
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)

        message.is_read = True
        message.read_at = timezone.now()
        message.save(update_fields=['is_read', 'read_at'])
        return Response({'status': 'read'})

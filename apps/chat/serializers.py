from rest_framework import serializers
from apps.chat.models import ChatRoom, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'id', 'room', 'sender', 'sender_name', 'content',
            'message_type', 'is_read', 'read_at', 'created_at', 'is_pii_blocked',
        ]
        read_only_fields = ['id', 'sender', 'sender_name', 'created_at', 'is_pii_blocked']

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username


class ChatRoomSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'student', 'student_name', 'teacher', 'teacher_name',
            'academy', 'created_at', 'last_message_at', 'last_message', 'unread_count',
        ]
        read_only_fields = ['id', 'created_at']

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name() or obj.teacher.username

    def get_last_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return {'content': msg.content, 'created_at': msg.created_at.isoformat()}
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if not request:
            return 0
        return obj.messages.filter(is_read=False).exclude(sender=request.user).count()

from django.contrib import admin
from .models import ChatRoom, ChatMessage, PIIViolationLog

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'academy', 'created_at', 'last_message_at')
    list_filter = ('academy', 'teacher', 'student')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'message_type', 'is_read', 'created_at', 'is_pii_blocked')
    list_filter = ('message_type', 'is_read', 'is_pii_blocked', 'room')
    search_fields = ('content', 'sender__username')

@admin.register(PIIViolationLog)
class PIIViolationLogAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'created_at')
    list_filter = ('room', 'sender')

from django.db import models
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ChatRoom(models.Model):
    """One-to-one chat room between a student and a teacher within an academy."""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='student_rooms', limit_choices_to={'role': 'student'}
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='teacher_rooms', limit_choices_to={'role': 'teacher'}
    )
    academy = models.ForeignKey(
        'academy.Academy', on_delete=models.CASCADE, related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'teacher')
        ordering = ['-last_message_at']

    def __str__(self):
        return f"Room: {self.student.username} <-> {self.teacher.username}"


class ChatMessage(models.Model):
    """A single message in a ChatRoom."""

    MESSAGE_TYPE_TEXT = 'text'
    MESSAGE_TYPE_IMAGE = 'image'
    MESSAGE_TYPE_LESSON_SUMMARY = 'lesson_summary'
    MESSAGE_TYPE_CHOICES = [
        (MESSAGE_TYPE_TEXT, 'Text'),
        (MESSAGE_TYPE_IMAGE, 'Image'),
        (MESSAGE_TYPE_LESSON_SUMMARY, 'Lesson Summary'),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    content = models.TextField(help_text="Sanitized / blocked content stored here")
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=MESSAGE_TYPE_TEXT)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pii_blocked = models.BooleanField(default=False, help_text="True if original content had PII")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.room}] {self.sender.username}: {self.content[:50]}"


class PIIViolationLog(models.Model):
    """Audit trail for PII violations caught by the chat filter."""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='pii_logs')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pii_violations'
    )
    original_content = models.TextField(help_text="The original message before substitution")
    detected_patterns = models.JSONField(help_text="List of pattern names that matched")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PII [{self.sender.username}] @ {self.created_at:%Y-%m-%d %H:%M}"

from django.db import models
from django.conf import settings

class FCMToken(models.Model):
    """Stores Firebase Cloud Messaging tokens for user devices."""
    DEVICE_TYPES = (
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, default='android')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.device_type} token"


class RingAlertLog(models.Model):
    """History of ring alerts sent by teachers to students."""
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, related_name='sent_ring_alerts')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='received_ring_alerts')
    message = models.TextField()
    audio_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Ring Alert from {self.teacher.user.username if self.teacher else 'Unknown'} to {self.student.user.username}"

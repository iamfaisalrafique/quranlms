from django.db import models
from django.conf import settings

class AttendanceRecord(models.Model):
    """Tracking attendance for students per class session."""
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'

    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='attendance_records')
    class_session = models.ForeignKey('lessons.ClassSession', on_delete=models.CASCADE, related_name='attendance_records', null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)
    
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='marked_attendance')
    marked_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'class_session', 'date')
        ordering = ['-date', '-marked_at']

    def __str__(self):
        return f"{self.student.user.username} - {self.status} on {self.date}"


class AttendanceStreak(models.Model):
    """Tracks consecutive days of attendance for gamification."""
    student = models.OneToOneField('accounts.StudentProfile', on_delete=models.CASCADE, related_name='streak')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_attendance_date = models.DateField(null=True, blank=True)
    grace_days_used = models.PositiveIntegerField(default=0)
    grace_days_banked = models.PositiveIntegerField(default=0, help_text="Grace days available to use")
    grace_days_allowed = models.PositiveIntegerField(default=3, help_text="Maximum banked grace days")

    def __str__(self):
        return f"{self.student.user.username}: {self.current_streak} days"

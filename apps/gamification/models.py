from django.db import models

class Badge(models.Model):
    """Represent an achievement badge that can be earned by students."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, help_text="Emoji icon for the badge")
    
    # Condition types: 'lesson_count', 'streak_days', 'quiz_count', 'perfect_score', 'etc'
    condition_type = models.CharField(max_length=50)
    condition_value = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.icon} {self.name}"


class StudentBadge(models.Model):
    """Link between a student and a badge they have earned."""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_to')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'badge')
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.student.user.username} earned {self.badge.name}"

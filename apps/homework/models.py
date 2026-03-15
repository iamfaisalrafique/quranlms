from django.db import models
from django.conf import settings

class Homework(models.Model):
    """Homework assigned by teachers."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    lesson_type = models.CharField(max_length=50, choices=[
        ('quran_recitation', 'Quran Recitation'),
        ('quran_memorization', 'Quran Memorization'),
        ('tajweed', 'Tajweed'),
        ('islamic_studies', 'Islamic Studies'),
        ('arabic_language', 'Arabic Language'),
    ])
    assigned_by = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE, related_name='created_homeworks')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HomeworkAssignment(models.Model):
    """Student-specific assignment of a homework task."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUBMITTED = 'submitted', 'Submitted'
        LATE = 'late', 'Late'
        GRADED = 'graded', 'Graded'

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='homework_assignments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    submitted_at = models.DateTimeField(null=True, blank=True)
    file_key = models.CharField(max_length=255, null=True, blank=True, help_text="R2/S3 file key for submission")
    
    grade = models.CharField(max_length=10, null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('homework', 'student')
        ordering = ['-due_date' if False else '-created_at'] # Sort by homework due date ideally

    def __str__(self):
        return f"{self.homework.title} - {self.student.user.username}"

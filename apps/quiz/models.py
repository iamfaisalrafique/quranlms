from django.db import models
from django.conf import settings

class Quiz(models.Model):
    """Quiz container for a set of questions."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    academy = models.ForeignKey('academy.Academy', on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_quizzes')
    
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Quran, Tajweed, Islamic History")
    pass_percentage = models.PositiveIntegerField(default=70)
    time_limit_minutes = models.PositiveIntegerField(default=0, help_text="0 for no limit")
    
    is_ai_generated = models.BooleanField(default=False)
    ai_topic = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    """A question within a quiz."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q: {self.text[:50]}"


class Choice(models.Model):
    """A multiple-choice option for a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]


class QuizAttempt(models.Model):
    """A student's attempt at taking a quiz."""
    class Status(models.TextChoices):
        STARTED = 'started', 'Started'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        PASSED = 'passed', 'Passed'

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='quiz_attempts')
    
    score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.STARTED)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.title} ({self.status})"


class AttemptAnswer(models.Model):
    """A student's selected answer for a specific question in an attempt."""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"Answer for {self.question.id}"

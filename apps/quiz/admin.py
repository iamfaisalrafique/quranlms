from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, AttemptAnswer

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'academy', 'category', 'is_ai_generated', 'created_at')
    list_filter = ('academy', 'category', 'is_ai_generated')
    search_fields = ('title', 'description')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'points', 'order')
    list_filter = ('quiz',)
    inlines = [ChoiceInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'status', 'started_at')
    list_filter = ('status', 'quiz', 'student')

@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_choice', 'is_correct')
    list_filter = ('is_correct',)

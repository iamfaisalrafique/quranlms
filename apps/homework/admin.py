from django.contrib import admin
from .models import Homework, HomeworkAssignment

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_type', 'assigned_by', 'due_date')
    list_filter = ('lesson_type', 'assigned_by', 'due_date')
    search_fields = ('title', 'description')

@admin.register(HomeworkAssignment)
class HomeworkAssignmentAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'status', 'grade', 'submitted_at')
    list_filter = ('status', 'homework', 'student')

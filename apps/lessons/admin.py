from django.contrib import admin
from .models import QuranBookmark, HadithBookmark, LessonLog, ClassSession

@admin.register(QuranBookmark)
class QuranBookmarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'ayat', 'created_at')
    list_filter = ('student', 'created_at')

@admin.register(HadithBookmark)
class HadithBookmarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'hadith', 'created_at')
    list_filter = ('student', 'created_at')

@admin.register(LessonLog)
class LessonLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'lesson_type', 'date', 'duration_minutes', 'rating')
    list_filter = ('lesson_type', 'date', 'teacher', 'student')
    search_fields = ('student__user__username', 'teacher__user__username', 'notes')

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'scheduled_at', 'duration_minutes', 'status')
    list_filter = ('status', 'teacher', 'scheduled_at')
    search_fields = ('teacher__user__username',)

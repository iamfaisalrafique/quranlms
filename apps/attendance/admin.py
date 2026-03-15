from django.contrib import admin
from .models import AttendanceRecord, AttendanceStreak

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_session', 'status', 'date')
    list_filter = ('status', 'date', 'student')

@admin.register(AttendanceStreak)
class AttendanceStreakAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_streak', 'longest_streak', 'last_attendance_date')
    search_fields = ('student__user__username',)

from django.contrib import admin
from .models import Badge, StudentBadge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'condition_type', 'condition_value')
    list_filter = ('condition_type',)

@admin.register(StudentBadge)
class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'earned_at')
    list_filter = ('badge', 'student', 'earned_at')

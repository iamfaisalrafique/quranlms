from django.contrib import admin
from .models import FCMToken, RingAlertLog

@admin.register(FCMToken)
class FCMTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_type', 'is_active', 'last_updated')
    list_filter = ('device_type', 'is_active')
    search_fields = ('user__username', 'token')

@admin.register(RingAlertLog)
class RingAlertLogAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'created_at', 'delivered')
    list_filter = ('delivered', 'teacher', 'student', 'created_at')

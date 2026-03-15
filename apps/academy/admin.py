from django.contrib import admin
from .models import Academy, AcademySettings

@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'owner', 'tier', 'is_active')
    list_filter = ('tier', 'is_active')
    search_fields = ('name', 'subdomain')

@admin.register(AcademySettings)
class AcademySettingsAdmin(admin.ModelAdmin):
    list_display = ('academy', 'whatsapp_enabled', 'ring_alert_enabled', 'ai_quiz_enabled')
    list_filter = ('whatsapp_enabled', 'ring_alert_enabled', 'ai_quiz_enabled')

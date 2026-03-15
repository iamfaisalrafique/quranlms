from django.db import models
from django.conf import settings

class Academy(models.Model):
    TIER_CHOICES = (
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('enterprise', 'Enterprise'),
    )
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_academies')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='starter')
    logo = models.ImageField(upload_to='academy_logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#1A6B4A')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class AcademySettings(models.Model):
    academy = models.OneToOneField(Academy, on_delete=models.CASCADE, related_name='settings')
    whatsapp_enabled = models.BooleanField(default=False)
    ring_alert_enabled = models.BooleanField(default=True)
    ai_quiz_enabled = models.BooleanField(default=True)
    google_workspace_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Settings for {self.academy.name}"

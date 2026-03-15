from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('register-device/', views.FCMTokenRegisterView.as_view(), name='register-device'),
    path('ring-alert/', views.RingAlertTriggerView.as_view(), name='trigger-ring-alert'),
    path('ring-alerts/', views.RingAlertHistoryView.as_view(), name='history-ring-alerts'),
]

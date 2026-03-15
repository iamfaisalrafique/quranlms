from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('certificate/generate/', views.CertificateGenerateView.as_view(), name='certificate-generate'),
    path('report-card/generate/', views.ReportCardGenerateView.as_view(), name='report-card-generate'),
]

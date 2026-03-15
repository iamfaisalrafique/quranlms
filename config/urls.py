from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/academy/', include('apps.academy.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/quran/', include('apps.quran.urls')),
    path('api/sunnah/', include('apps.sunnah.urls')),
    path('api/lessons/', include('apps.lessons.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/homework/', include('apps.homework.urls')),
    path('api/quiz/', include('apps.quiz.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/billing/', include('apps.billing.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    
    # Catch-all for React Frontend
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('mark/', views.MarkAttendanceView.as_view(), name='mark'),
    path('student/<int:student_id>/monthly/', views.StudentMonthlyAttendanceView.as_view(), name='student-monthly'),
    path('student/<int:student_id>/stats/', views.StudentAttendanceStatsView.as_view(), name='student-stats'),
]

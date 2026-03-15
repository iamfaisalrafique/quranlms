from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('log/', views.LessonLogCreateView.as_view(), name='log-create'),
    path('student/<int:student_id>/', views.StudentLessonHistoryView.as_view(), name='student-history'),
    path('teacher/', views.TeacherLessonLogView.as_view(), name='teacher-logs'),
    path('class/schedule/', views.ClassSessionScheduleView.as_view(), name='class-schedule'),
]

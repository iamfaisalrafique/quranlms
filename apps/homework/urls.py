from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('assign/', views.AssignHomeworkView.as_view(), name='assign'),
    path('<int:pk>/submit/', views.SubmitHomeworkView.as_view(), name='submit'),
    path('<int:pk>/grade/', views.GradeHomeworkView.as_view(), name='grade'),
]

from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='list'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='detail'),
    path('ai-generate/', views.AIGenerateQuizView.as_view(), name='ai-generate'),
    path('<int:pk>/start/', views.QuizAttemptStartView.as_view(), name='start-attempt'),
    path('attempt/<int:pk>/submit/', views.QuizAttemptSubmitView.as_view(), name='submit-attempt'),
]

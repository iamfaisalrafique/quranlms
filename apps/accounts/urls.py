from django.urls import path
from . import views

urlpatterns = [
    path('auth/student/login/',    views.StudentLoginView.as_view(),    name='student-login'),
    path('auth/login/',            views.UnifiedLoginView.as_view(),    name='login'),
    path('auth/parent/login/',     views.ParentLoginView.as_view(),     name='parent-login'),
    path('auth/refresh/',          views.RefreshView.as_view(),         name='token-refresh'),
    path('auth/logout/',           views.LogoutView.as_view(),          name='logout'),
    path('auth/me/',               views.MeView.as_view(),              name='me'),
    path('auth/google/',           views.GoogleAuthView.as_view(),      name='google-auth'),
    path('auth/set-guardian-pin/', views.SetGuardianPinView.as_view(),  name='set-guardian-pin'),
]

from rest_framework import generics, permissions
from .models import LessonLog, ClassSession
from .serializers import LessonLogSerializer, ClassSessionSerializer
from apps.accounts.permissions import IsTeacher, IsStudent
from apps.gamification.utils import check_and_award_badges
from .google_workspace import create_meet_space, create_calendar_event, send_calendar_invites
import datetime


class LessonLogCreateView(generics.CreateAPIView):
    """POST /api/lessons/log/ — teacher logs lesson."""
    queryset = LessonLog.objects.all()
    serializer_class = LessonLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        lesson_log = serializer.save(teacher=self.request.user.teacher_profile)
        check_and_award_badges(lesson_log.student)


class StudentLessonHistoryView(generics.ListAPIView):
    """GET /api/lessons/student/{id}/ — student lesson history."""
    serializer_class = LessonLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        # Students can only see their own history, Teachers/Admins can see any
        if self.request.user.role == 'student' and self.request.user.student_profile.id != int(student_id):
            return LessonLog.objects.none()
        return LessonLog.objects.filter(student_id=student_id).select_related('student__user', 'teacher__user')


class TeacherLessonLogView(generics.ListAPIView):
    """GET /api/lessons/teacher/ — teacher's lesson logs."""
    serializer_class = LessonLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return LessonLog.objects.filter(teacher=self.request.user.teacher_profile).select_related('student__user', 'teacher__user')

class ClassSessionScheduleView(generics.CreateAPIView):
    """POST /api/lessons/class/schedule/ — Schedule a class."""
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        # Create Google Meet space
        # Mock token representing the authenticated teacher's OAuth scopes
        mock_token = "mock_teacher_oauth_token" 
        meet_url, meet_id = create_meet_space(mock_token)
        
        # Determine schedule time (defaulting to 1 hour from now if not provided, just as a fail-safe)
        scheduled_at = self.request.data.get('scheduled_at')
        if not scheduled_at:
            scheduled_at = datetime.datetime.now() + datetime.timedelta(hours=1)
            
        student_ids = self.request.data.get('students', [])
        
        # Save session with meet details
        session = serializer.save(
            teacher=teacher,
            google_meet_url=meet_url,
            google_meet_id=meet_id,
            status='scheduled'
        )
        
        # Create calendar event
        event_id = create_calendar_event(mock_token, meet_url, scheduled_at, duration_mins=session.duration_minutes)
        session.google_calendar_event_id = event_id
        session.save()
        
        # Connect students & send invites
        if student_ids:
            session.students.set(student_ids)
            student_emails = [s.user.email for s in session.students.all()]
            send_calendar_invites(mock_token, event_id, student_emails)

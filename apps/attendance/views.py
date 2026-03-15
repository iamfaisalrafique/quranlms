from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import AttendanceRecord, AttendanceStreak
from .serializers import AttendanceRecordSerializer, AttendanceStreakSerializer
from apps.accounts.permissions import IsTeacher, IsStudent
from apps.gamification.utils import check_and_award_badges
import datetime


class MarkAttendanceView(generics.CreateAPIView):
    """POST /api/attendance/mark/ — mark attendance."""
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        attendance_record = serializer.save(marked_by=self.request.user)
        check_and_award_badges(attendance_record.student)


class StudentMonthlyAttendanceView(generics.ListAPIView):
    """GET /api/attendance/student/{id}/monthly/ — calendar grid (dummy simple list for now)."""
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        month = self.request.query_params.get('month', datetime.date.today().month)
        year = self.request.query_params.get('year', datetime.date.today().year)
        
        return AttendanceRecord.objects.filter(
            student_id=student_id,
            date__year=year,
            date__month=month
        )


class StudentAttendanceStatsView(APIView):
    """GET /api/attendance/student/{id}/stats/ — % + streak."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        total = AttendanceRecord.objects.filter(student_id=student_id).count()
        present = AttendanceRecord.objects.filter(student_id=student_id, status='present').count()
        
        percentage = (present / total * 100) if total > 0 else 0
        
        try:
            streak_obj = AttendanceStreak.objects.get(student_id=student_id)
            streak = streak_obj.current_streak
            longest = streak_obj.longest_streak
        except AttendanceStreak.DoesNotExist:
            streak = 0
            longest = 0
            
        return Response({
            'total_classes': total,
            'present_classes': present,
            'attendance_percentage': round(percentage, 2),
            'current_streak': streak,
            'longest_streak': longest
        })

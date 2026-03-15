from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from apps.accounts.models import StudentProfile
from apps.accounts.permissions import IsTeacher, IsAcademyAdmin
from .certificate import generate_achievement_certificate
from .report_card import generate_student_report_card

class CertificateGenerateView(APIView):
    """POST /api/reports/certificate/generate/"""
    permission_classes = [permissions.IsAuthenticated, IsTeacher | IsAcademyAdmin]

    def post(self, request):
        student_id = request.data.get('student_id')
        achievement = request.data.get('achievement', 'For outstanding performance in Quran studies.')
        
        student = get_object_or_404(StudentProfile, id=student_id)
        teacher_name = request.user.get_full_name()
        
        try:
            url = generate_achievement_certificate(
                student, 
                student.academy, 
                achievement, 
                teacher_name
            )
            return Response({'pdf_url': url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportCardGenerateView(APIView):
    """POST /api/reports/report-card/generate/"""
    permission_classes = [permissions.IsAuthenticated, IsTeacher | IsAcademyAdmin]

    def post(self, request):
        student_id = request.data.get('student_id')
        student = get_object_or_404(StudentProfile, id=student_id)
        
        try:
            url = generate_student_report_card(student)
            return Response({'pdf_url': url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.shortcuts import get_object_or_404
from apps.accounts.models import StudentProfile
from apps.accounts.permissions import IsTeacher
from .models import FCMToken, RingAlertLog
from .serializers import FCMTokenSerializer, RingAlertLogSerializer
from .ring_alert import send_ring_alert

class FCMTokenRegisterView(APIView):
    """POST /api/notifications/register-device/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        device_type = request.data.get('device_type', 'android')
        
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        fcm_token, created = FCMToken.objects.update_or_create(
            user=request.user,
            token=token,
            defaults={'device_type': device_type, 'is_active': True}
        )
        
        return Response({'status': 'registered'}, status=status.HTTP_200_OK)


class RingAlertTriggerView(APIView):
    """POST /api/notifications/ring-alert/"""
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    
    def post(self, request):
        student_id = request.data.get('student_id')
        message = request.data.get('message', 'Please join the class now.')
        
        student = get_object_or_404(StudentProfile, id=student_id)
        teacher = request.user.teacher_profile
        
        log_entry = send_ring_alert(teacher, student, message)
        
        return Response(RingAlertLogSerializer(log_entry).data, status=status.HTTP_201_CREATED)


class RingAlertHistoryView(generics.ListAPIView):
    """GET /api/notifications/ring-alerts/"""
    serializer_class = RingAlertLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    
    def get_queryset(self):
        return RingAlertLog.objects.filter(
            teacher=self.request.user.teacher_profile
        ).order_by('-created_at')

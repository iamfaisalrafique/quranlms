from rest_framework import serializers
from .models import FCMToken, RingAlertLog
from apps.accounts.serializers import StudentProfileSerializer, TeacherProfileSerializer

class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ['token', 'device_type']

class RingAlertLogSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = RingAlertLog
        fields = ['id', 'teacher', 'student', 'message', 'audio_url', 'created_at', 'delivered']
        read_only_fields = ['audio_url', 'created_at', 'delivered']

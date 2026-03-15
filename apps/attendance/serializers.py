from rest_framework import serializers
from .models import AttendanceRecord, AttendanceStreak


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'
        read_only_fields = ['id', 'marked_at', 'date']


class AttendanceStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceStreak
        fields = '__all__'
        read_only_fields = ['id', 'student']

from rest_framework import serializers
from .models import LessonLog, ClassSession


class LessonLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = LessonLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ClassSessionSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = ClassSession
        fields = '__all__'
        read_only_fields = ['id']

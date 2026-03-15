from rest_framework import serializers
from .models import Homework, HomeworkAssignment


class HomeworkSerializer(serializers.ModelSerializer):
    assigned_by_name = serializers.CharField(source='assigned_by.user.get_full_name', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class HomeworkAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    homework_title = serializers.CharField(source='homework.title', read_only=True)

    class Meta:
        model = HomeworkAssignment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'submitted_at']

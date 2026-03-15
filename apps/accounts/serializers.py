import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import StudentProfile, TeacherProfile, ParentProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'avatar']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id', 'academy', 'teacher',
                  'guardian_name', 'guardian_phone', 'guardian_email']


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'academy', 'subjects', 'bio', 'google_meet_link']


class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ParentProfile
        fields = ['id', 'user', 'students']


# ── Login Serializers ──────────────────────────────────────────────────────────

class StudentLoginSerializer(serializers.Serializer):
    """Validates student_id in STU-XXXX format (code-based login, no password)."""
    student_id = serializers.CharField()

    def validate_student_id(self, value):
        value = value.strip().upper()
        if not re.match(r'^STU-\d{4}$', value):
            raise serializers.ValidationError(
                "Invalid student ID format. Expected STU-XXXX (e.g. STU-0001)."
            )
        return value


class UnifiedLoginSerializer(serializers.Serializer):
    """Username + password login for all roles."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ParentLoginSerializer(serializers.Serializer):
    """student_id + guardian_pin login for parents (read-only access)."""
    student_id = serializers.CharField()
    guardian_pin = serializers.CharField(write_only=True)

    def validate_student_id(self, value):
        value = value.strip().upper()
        if not re.match(r'^STU-\d{4}$', value):
            raise serializers.ValidationError(
                "Invalid student ID format. Expected STU-XXXX."
            )
        return value

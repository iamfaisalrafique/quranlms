import logging
import bcrypt

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import StudentProfile, TeacherProfile, ParentProfile
from .serializers import (
    UserSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    ParentProfileSerializer,
    StudentLoginSerializer,
    UnifiedLoginSerializer,
    ParentLoginSerializer,
)
from .google_auth import exchange_code_for_token, get_google_user_info

User = get_user_model()
logger = logging.getLogger(__name__)


def _jwt_pair(user):
    """Return a dict with access + refresh JWT tokens for the given user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


# ── Student Login ─────────────────────────────────────────────────────────────
class StudentLoginView(APIView):
    """
    POST /api/auth/student/login/
    Accepts STU-XXXX student_id (no password — replicates PHP code-based login).
    Returns JWT pair + full student profile.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data['student_id']

        try:
            profile = StudentProfile.objects.select_related('user', 'academy').get(
                student_id=student_id
            )
        except StudentProfile.DoesNotExist:
            logger.warning("Student login failed: student_id=%s not found", student_id)
            return Response(
                {"detail": "Invalid student ID."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = profile.user
        tokens = _jwt_pair(user)
        logger.info("Student logged in: %s", student_id)

        return Response({
            **tokens,
            "user": UserSerializer(user).data,
            "profile": StudentProfileSerializer(profile).data,
        })


# ── Unified Login ─────────────────────────────────────────────────────────────
class UnifiedLoginView(APIView):
    """
    POST /api/auth/login/
    Username + password login for all roles (Teacher, Admin, etc).
    Returns JWT pair + profile.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UnifiedLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            logger.warning("Login failed: wrong password for %s", username)
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        tokens = _jwt_pair(user)
        logger.info("User logged in: %s with role: %s", username, user.role)

        profile_data = None
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            profile_data = TeacherProfileSerializer(user.teacher_profile).data
        elif user.role == 'student' and hasattr(user, 'student_profile'):
            profile_data = StudentProfileSerializer(user.student_profile).data
        elif user.role == 'parent' and hasattr(user, 'parent_profile'):
            profile_data = ParentProfileSerializer(user.parent_profile).data

        return Response({
            **tokens,
            "user": UserSerializer(user).data,
            "profile": profile_data,
        })


# ── Parent Login ──────────────────────────────────────────────────────────────
class ParentLoginView(APIView):
    """
    POST /api/auth/parent/login/
    student_id + guardian_pin → read-only JWT with role=parent.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ParentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data['student_id']
        guardian_pin = serializer.validated_data['guardian_pin'].encode()

        try:
            student = StudentProfile.objects.select_related('user').get(
                student_id=student_id
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Invalid student ID or PIN."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Verify bcrypt PIN
        pin_hash = student.guardian_pin.encode()
        if not bcrypt.checkpw(guardian_pin, pin_hash):
            logger.warning("Parent login failed: wrong PIN for student %s", student_id)
            return Response(
                {"detail": "Invalid student ID or PIN."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Find or create the ParentProfile user
        parent_profile = student.parents.first()
        if not parent_profile:
            return Response(
                {"detail": "No parent account linked to this student."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = parent_profile.user
        tokens = _jwt_pair(user)
        logger.info("Parent logged in for student: %s", student_id)

        return Response({
            **tokens,
            "user": UserSerializer(user).data,
            "profile": ParentProfileSerializer(parent_profile).data,
        })


# ── Token Refresh ─────────────────────────────────────────────────────────────
class RefreshView(APIView):
    """POST /api/auth/refresh/ — exchanges a refresh token for a new access token."""
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            return Response({"access": str(token.access_token)})
        except TokenError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)


# ── Logout (blacklist refresh token) ─────────────────────────────────────────
class LogoutView(APIView):
    """POST /api/auth/logout/ — blacklists the refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User %s logged out", request.user.username)
            return Response({"detail": "Logged out successfully."})
        except TokenError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


# ── Me ────────────────────────────────────────────────────────────────────────
class MeView(APIView):
    """GET /api/auth/me/ — returns current user + role-specific profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {"user": UserSerializer(user).data, "profile": None}

        if user.role == 'student' and hasattr(user, 'student_profile'):
            data["profile"] = StudentProfileSerializer(user.student_profile).data
        elif user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            data["profile"] = TeacherProfileSerializer(user.teacher_profile).data
        elif user.role == 'parent' and hasattr(user, 'parent_profile'):
            data["profile"] = ParentProfileSerializer(user.parent_profile).data

        return Response(data)


# ── Google OAuth ──────────────────────────────────────────────────────────────
class GoogleAuthView(APIView):
    """
    POST /api/auth/google/
    Accepts a Google OAuth2 authorization code.
    Creates or updates a Teacher user (Google OAuth is teacher-only).
    Stores the Google refresh token on the TeacherProfile for Meet/Calendar.
    Returns JWT pair.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code", "").strip()
        if not code:
            return Response(
                {"detail": "Google OAuth code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tokens = exchange_code_for_token(code)
            google_user = get_google_user_info(tokens["access_token"])
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        email = google_user["email"].lower()
        name_parts = google_user.get("name", "").split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Find by email; create if first login
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": "teacher",
            },
        )
        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=["first_name", "last_name"])

        # Store Google refresh token on the TeacherProfile if available
        google_refresh = tokens.get("refresh_token", "")
        if google_refresh and hasattr(user, 'teacher_profile'):
            profile = user.teacher_profile
            profile.google_refresh_token = google_refresh
            profile.save(update_fields=["google_refresh_token"])

        jwt_tokens = _jwt_pair(user)
        logger.info("Google OAuth login: %s (new=%s)", email, created)

        profile_data = None
        if hasattr(user, 'teacher_profile'):
            profile_data = TeacherProfileSerializer(user.teacher_profile).data

        return Response({
            **jwt_tokens,
            "user": UserSerializer(user).data,
            "profile": profile_data,
            "created": created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ── Set Guardian PIN ──────────────────────────────────────────────────────────
class SetGuardianPinView(APIView):
    """
    POST /api/auth/set-guardian-pin/
    Teacher or admin sets a PIN for a student's guardian.
    PIN is bcrypt-hashed before storage.
    Body: { student_id: "STU-0001", pin: "123456" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from .permissions import IsTeacherOrAdmin
        if not (request.user.role in ('teacher', 'admin')):
            return Response(
                {"detail": "Only teachers or admins can set guardian PINs."},
                status=status.HTTP_403_FORBIDDEN,
            )

        student_id = request.data.get("student_id", "").strip().upper()
        pin = request.data.get("pin", "").strip()

        if not re.match(r'^STU-\d{4}$', student_id):
            return Response(
                {"detail": "Invalid student ID format."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(pin) < 4:
            return Response(
                {"detail": "PIN must be at least 4 digits."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            profile = StudentProfile.objects.get(student_id=student_id)
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Student not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        import re as _re
        hashed = bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()
        profile.guardian_pin = hashed
        profile.save(update_fields=["guardian_pin"])

        logger.info("Guardian PIN set for student %s by %s", student_id, request.user.username)
        return Response({"detail": "Guardian PIN set successfully."})

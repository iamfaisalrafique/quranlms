from rest_framework.permissions import BasePermission, IsAuthenticated


class IsStudent(BasePermission):
    """Allow access only to authenticated users with role=student."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'student'
        )


class IsTeacher(BasePermission):
    """Allow access only to authenticated users with role=teacher."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'teacher'
        )


class IsParent(BasePermission):
    """Allow access only to authenticated users with role=parent (read-only token)."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'parent'
        )


class IsAcademyAdmin(BasePermission):
    """Allow access only to admin users."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsSystemAdmin(BasePermission):
    """Django superuser / system-level admin."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsTeacherOrAdmin(BasePermission):
    """Allow teacher or admin — useful for shared management views."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('teacher', 'admin')
        )


class AcademyScopedPermission(BasePermission):
    """
    Ensures the authenticated user belongs to the same academy as the object
    being accessed. Must be used with a view that sets view.get_academy_id().
    Falls back to True for superusers.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Resolve the user's academy id
        user = request.user
        user_academy_id = None
        if hasattr(user, 'student_profile'):
            user_academy_id = user.student_profile.academy_id
        elif hasattr(user, 'teacher_profile'):
            user_academy_id = user.teacher_profile.academy_id

        # Resolve the object's academy id
        obj_academy_id = getattr(obj, 'academy_id', None)

        if user_academy_id is None or obj_academy_id is None:
            return False
        return user_academy_id == obj_academy_id

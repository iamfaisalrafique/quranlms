from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Homework, HomeworkAssignment
from .serializers import HomeworkSerializer, HomeworkAssignmentSerializer
from apps.accounts.permissions import IsTeacher, IsStudent


class AssignHomeworkView(generics.CreateAPIView):
    """POST /api/homework/assign/ — teacher assigns homework."""
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user.teacher_profile)


class SubmitHomeworkView(generics.UpdateAPIView):
    """POST /api/homework/{id}/submit/ — student submits (using PATCH actually)."""
    queryset = HomeworkAssignment.objects.all()
    serializer_class = HomeworkAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        if assignment.student != request.user.student_profile:
            return Response({'detail': 'Not your assignment.'}, status=status.HTTP_403_FORBIDDEN)
            
        assignment.status = 'submitted'
        if assignment.homework.due_date < timezone.now():
            assignment.status = 'late'
            
        assignment.submitted_at = timezone.now()
        assignment.file_key = request.data.get('file_key')
        assignment.save()
        
        return Response(self.get_serializer(assignment).data)


class GradeHomeworkView(generics.UpdateAPIView):
    """PATCH /api/homework/{id}/grade/ — teacher grades."""
    queryset = HomeworkAssignment.objects.all()
    serializer_class = HomeworkAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        # Ensure assignment homework was created by this teacher or academy Admin
        # Simplification: any teacher for now
        
        assignment.status = 'graded'
        assignment.grade = request.data.get('grade')
        assignment.feedback = request.data.get('feedback', '')
        assignment.save()
        
        return Response(self.get_serializer(assignment).data)

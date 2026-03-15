import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    academy = models.ForeignKey('academy.Academy', on_delete=models.CASCADE, related_name='students')
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    guardian_name = models.CharField(max_length=255)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField()
    guardian_pin = models.CharField(max_length=128) # Fingerprint/Hash
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            # Academy-scoped STU-XXXX: each academy restarts from STU-0001
            last_student = (
                StudentProfile.objects.filter(academy=self.academy)
                .order_by('id')
                .last()
            )
            if not last_student:
                self.student_id = 'STU-0001'
            else:
                last_id = int(last_student.student_id.split('-')[1])
                self.student_id = f'STU-{(last_id + 1):04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    academy = models.ForeignKey('academy.Academy', on_delete=models.CASCADE, related_name='teachers')
    subjects = models.JSONField(default=list) # e.g. ["Quran", "Hifz"]
    bio = models.TextField(blank=True)
    google_meet_link = models.URLField(blank=True)
    # Stored after Google OAuth consent — used for Meet/Calendar API calls
    google_refresh_token = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.academy.name}"

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    students = models.ManyToManyField(StudentProfile, related_name='parents')
    pin_hash = models.CharField(max_length=128)
    
    def __str__(self):
        return f"Parent: {self.user.username}"

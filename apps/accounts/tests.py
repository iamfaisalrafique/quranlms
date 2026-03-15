from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.academy.models import Academy
from apps.accounts.models import TeacherProfile

User = get_user_model()

class TeacherLoginTests(APITestCase):
    def setUp(self):
        self.academy = Academy.objects.create(
            name="Test Academy",
            subdomain="test",
            owner=User.objects.create_user(username="owner", email="owner@example.com", password="password123")
        )
        self.teacher_user = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="password123",
            role="teacher"
        )
        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            academy=self.academy
        )
        self.url = reverse('teacher-login')

    def test_teacher_login_success(self):
        data = {
            "email": "teacher@example.com",
            "password": "password123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], "teacher@example.com")
        self.assertEqual(response.data['profile']['id'], self.teacher_profile.id)

    def test_teacher_login_invalid_password(self):
        data = {
            "email": "teacher@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Invalid credentials.")

    def test_teacher_login_invalid_email(self):
        data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Invalid credentials.")

    def test_teacher_login_wrong_role(self):
        student_user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password123",
            role="student"
        )
        data = {
            "email": "student@example.com",
            "password": "password123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Invalid credentials.")

    def test_teacher_login_invalid_data(self):
        data = {
            "email": "not-an-email",
            "password": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

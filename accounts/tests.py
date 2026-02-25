from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration_success(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        User.objects.create_user(username='loginuser', password='TestPass123!')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser',
            'password': 'TestPass123!',
        })
        self.assertIn(response.status_code, [200, 302])

    def test_wrong_password_fails(self):
        User.objects.create_user(username='failuser', password='CorrectPass123!')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'failuser',
            'password': 'WrongPassword!',
        })
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertIn(response.status_code, [302, 403])

    def test_authenticated_user_can_view_profile(self):
        user = User.objects.create_user(username='profileuser', password='TestPass123!')
        self.client.login(username='profileuser', password='TestPass123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

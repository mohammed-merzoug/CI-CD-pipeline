from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class DashboardAccessTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin', password='AdminPass123!', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular', password='UserPass123!'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertIn(response.status_code, [302, 403])

    def test_regular_user_cannot_access_dashboard(self):
        self.client.login(username='regular', password='UserPass123!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertIn(response.status_code, [302, 403])

    def test_admin_can_access_dashboard(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_product_list(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.get(reverse('dashboard:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_category_list(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.get(reverse('dashboard:category_list'))
        self.assertEqual(response.status_code, 200)

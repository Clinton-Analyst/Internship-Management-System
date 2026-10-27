from django.test import TestCase
from django.urls import reverse
from .models import User


class DayTwoAccountTests(TestCase):
    def test_admin_add_user_form_includes_role(self):
        admin_user = User.objects.create_superuser(
            username="siteadmin",
            email="admin@example.com",
            password="test-password-123",
        )
        self.client.force_login(admin_user)

        response = self.client.get(reverse("admin:accounts_user_add"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="role"')

    def test_login_shows_user_name_and_role_on_home(self):
        User.objects.create_user(
            username="student1",
            password="test-password-123",
            first_name="Sam",
            role=User.STUDENT,
        )

        response = self.client.post(
            reverse("login"),
            {"username": "student1", "password": "test-password-123"},
        )

        self.assertRedirects(response, reverse("home"))
        home_response = self.client.get(reverse("home"))
        self.assertContains(home_response, "Hello Sam, role: student")

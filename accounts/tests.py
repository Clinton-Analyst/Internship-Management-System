from django.test import TestCase
from django.urls import reverse
from .models import User
from placements.models import Placement, StudentProfile, SupervisorProfile


class DayTwoAccountTests(TestCase):
    def test_login_links_to_student_registration(self):
        response = self.client.get(reverse("login"))

        self.assertContains(response, reverse("register"))
        self.assertContains(response, "Create an account")

    def test_registration_creates_student_without_placement(self):
        response = self.client.post(reverse("register"), {
            "username": "newstudent",
            "first_name": "New",
            "last_name": "Student",
            "email": "newstudent@example.com",
            "password1": "Test-registration-pass-482!",
            "password2": "Test-registration-pass-482!",
        })

        user = User.objects.get(username="newstudent")
        profile = StudentProfile.objects.get(user=user)
        self.assertEqual(user.role, User.STUDENT)
        self.assertFalse(Placement.objects.filter(student=profile).exists())
        self.assertRedirects(response, reverse("profile"))
        self.assertEqual(self.client.get(reverse("profile")).status_code, 200)

    def test_login_links_to_supervisor_registration(self):
        response = self.client.get(reverse("login"))

        self.assertContains(response, reverse("register_supervisor"))
        self.assertContains(response, "Register here")

    def test_supervisor_registration_creates_profile_without_elevating_role(self):
        response = self.client.post(reverse("register_supervisor"), {
            "username": "newsupervisor",
            "first_name": "New",
            "last_name": "Supervisor",
            "email": "supervisor@example.com",
            "organisation": "Example Organisation",
            "phone": "+254 700 000000",
            "password1": "Test-supervisor-pass-482!",
            "password2": "Test-supervisor-pass-482!",
            "role": User.ADMIN,
            "is_superuser": "on",
        })

        user = User.objects.get(username="newsupervisor")
        profile = SupervisorProfile.objects.get(user=user)
        self.assertEqual(user.role, User.SUPERVISOR)
        self.assertFalse(user.is_superuser)
        self.assertEqual(profile.organisation, "Example Organisation")
        self.assertEqual(profile.phone, "+254 700 000000")
        self.assertRedirects(response, reverse("sup_reports"))

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

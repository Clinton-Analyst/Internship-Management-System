from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class AdminListPageTests(TestCase):
    def test_admin_list_pages_render(self):
        admin = User.objects.create_user(
            username="listadmin",
            password="test-password-123",
            role=User.ADMIN,
        )
        self.client.force_login(admin)

        for page_name in ("students", "supervisors", "tracks", "placements"):
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)

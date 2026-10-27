from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    STUDENT, SUPERVISOR, ADMIN = "student", "supervisor", "admin"
    ROLES = [(STUDENT, "Student"), (SUPERVISOR, "Supervisor"), (ADMIN, "Administrator")]
    role = models.CharField(max_length=12, choices=ROLES, default=STUDENT)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.get_full_name() or self.username


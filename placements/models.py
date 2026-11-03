import math
from datetime import date
from django.conf import settings
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    reg_number = models.CharField("Registration number", max_length=30, blank=True)
    programme = models.CharField(max_length=120, blank=True)
    department = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.display_name

class SupervisorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supervisor_profile")
    organisation = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.display_name

class Track(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Placement(models.Model):
    PLACED, ACTIVE, COMPLETED = "placed", "active", "completed"
    STATUSES = [(PLACED, "Placed"), (ACTIVE, "Active"), (COMPLETED, "Completed")]

    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="placement")
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.PROTECT, related_name="placements")
    track = models.ForeignKey(Track, on_delete=models.PROTECT, related_name="placements")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUSES, default=PLACED)

    def __str__(self):
        return f"{self.student} -> {self.track}"

    # ---- progress maths (Day 5): how many weeks "played" vs reports "scored" ----
    def total_weeks(self):
        return max(1, math.ceil(((self.end_date - self.start_date).days + 1) / 7))

    def expected_weeks(self, today=None):
        today = today or date.today()
        if today < self.start_date:
            return 0
        elapsed = (min(today, self.end_date) - self.start_date).days // 7
        return min(elapsed, self.total_weeks())

    def submitted_weeks(self):
        return len(self.reports.all())

    def missing_weeks(self):
        return max(0, self.expected_weeks() - self.submitted_weeks())

    def flag(self):
        if self.status == self.COMPLETED:
            return "completed"
        m = self.missing_weeks()
        return "on_track" if m == 0 else "overdue" if m == 1 else "at_risk"


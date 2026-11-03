from django.db import models
from placements.models import Placement

class WeeklyReport(models.Model):
    SUBMITTED, REVIEWED = "submitted", "reviewed"
    STATUSES = [(SUBMITTED, "Pending review"), (REVIEWED, "Reviewed")]

    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name="reports")
    week_number = models.PositiveSmallIntegerField()
    activities = models.TextField("Activities completed")
    skills_learned = models.TextField()
    challenges = models.TextField("Challenges faced")
    status = models.CharField(max_length=10, choices=STATUSES, default=SUBMITTED)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["week_number"]
        constraints = [models.UniqueConstraint(fields=["placement", "week_number"], name="one_report_per_week")]

    def __str__(self):
        return f"{self.placement.student} - Week {self.week_number}"


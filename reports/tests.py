from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from placements.models import StudentProfile, SupervisorProfile, Track, Placement
from reports.models import WeeklyReport

PW = "pw12345!Xy"

class FlowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin1", password=PW, role="admin")
        self.sup_user = User.objects.create_user("sup1", password=PW, role="supervisor")
        self.sup = SupervisorProfile.objects.create(user=self.sup_user)
        self.other_sup = SupervisorProfile.objects.create(user=User.objects.create_user("sup2", password=PW, role="supervisor"))
        self.stu_user = User.objects.create_user("stu1", password=PW, role="student")
        self.stu = StudentProfile.objects.create(user=self.stu_user)
        self.track = Track.objects.create(name="Backend")
        self.pl = Placement.objects.create(student=self.stu, supervisor=self.sup, track=self.track,
            start_date=date.today() - timedelta(days=21), end_date=date.today() + timedelta(days=60), status="active")

    def test_role_guards(self):
        self.client.login(username="stu1", password=PW)
        self.assertEqual(self.client.get(reverse("admin_dashboard")).status_code, 403)
        self.assertEqual(self.client.get(reverse("sup_reports")).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.get(reverse("my_reports")).status_code, 302)  # to login

    def test_report_feedback_loop(self):
        self.client.login(username="stu1", password=PW)
        data = {"week_number": 1, "activities": "Built API", "skills_learned": "Django", "challenges": "None"}
        self.assertEqual(self.client.post(reverse("report_new"), data).status_code, 302)
        r = WeeklyReport.objects.get()
        self.assertEqual(r.status, "submitted")
        self.client.post(reverse("report_new"), data)           # duplicate week rejected
        self.assertEqual(WeeklyReport.objects.count(), 1)
        self.client.logout(); self.client.login(username="sup1", password=PW)
        self.client.post(reverse("report_review", args=[r.pk]), {"feedback": "Good work, add tests."})
        r.refresh_from_db(); self.assertEqual(r.status, "reviewed")
        self.client.logout(); self.client.login(username="stu1", password=PW)
        self.client.post(reverse("report_edit", args=[r.pk]), {**data, "activities": "Built API + tests"})
        r.refresh_from_db(); self.assertEqual(r.status, "submitted")   # resubmit resets

    def test_supervisor_cannot_review_others(self):
        r = WeeklyReport.objects.create(placement=self.pl, week_number=1, activities="a", skills_learned="b", challenges="c")
        self.client.login(username="sup2", password=PW)
        self.assertEqual(self.client.get(reverse("report_review", args=[r.pk])).status_code, 404)

    def test_flags(self):
        self.assertEqual(self.pl.expected_weeks(), 3)
        self.assertEqual(self.pl.flag(), "at_risk")
        for w in (1, 2):
            WeeklyReport.objects.create(placement=self.pl, week_number=w, activities="a", skills_learned="b", challenges="c")
        self.assertEqual(self.pl.flag(), "overdue")
        WeeklyReport.objects.create(placement=self.pl, week_number=3, activities="a", skills_learned="b", challenges="c")
        self.assertEqual(self.pl.flag(), "on_track")

    def test_admin_dashboard_and_placement_form(self):
        self.client.login(username="admin1", password=PW)
        self.assertEqual(self.client.get(reverse("admin_dashboard")).status_code, 200)
        bad = {"student": self.stu.pk, "supervisor": self.sup.pk, "track": self.track.pk,
               "start_date": "2026-05-10", "end_date": "2026-05-01", "status": "placed"}
        self.assertContains(self.client.post(reverse("placement_new"), bad), "End date must be after")


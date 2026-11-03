from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import User
from placements.models import Placement, StudentProfile, SupervisorProfile
from reports.models import WeeklyReport

@role_required("admin")
def admin_dashboard(request):
    placements = list(Placement.objects.select_related("student__user", "supervisor__user", "track")
                      .prefetch_related("reports"))
    order = {"at_risk": 0, "overdue": 1, "on_track": 2, "completed": 3}
    placements.sort(key=lambda p: order[p.flag()])
    rows = [{"p": p, "flag": p.flag(), "submitted": p.submitted_weeks(),
             "expected": p.expected_weeks(), "missing": p.missing_weeks()} for p in placements]
    unplaced = StudentProfile.objects.filter(placement__isnull=True).select_related("user")
    return render(request, "dashboard/admin_dashboard.html", {
        "rows": rows, "unplaced": unplaced,
        "stats": {
            "students": StudentProfile.objects.count(),
            "supervisors": SupervisorProfile.objects.count(),
            "active": sum(1 for p in placements if p.status != Placement.COMPLETED),
            "pending": WeeklyReport.objects.filter(status=WeeklyReport.SUBMITTED).count(),
            "at_risk": sum(1 for r in rows if r["flag"] == "at_risk"),
        },
    })


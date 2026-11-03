from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from accounts.decorators import role_required
from placements.models import Placement
from .forms import ReportForm, ReviewForm
from .models import WeeklyReport

def _my_placement(user):
    return Placement.objects.filter(student__user=user).select_related("supervisor__user", "track").first()

@role_required("student")
def my_reports(request):
    placement = _my_placement(request.user)
    reports = placement.reports.all() if placement else []
    return render(request, "reports/my_reports.html", {"placement": placement, "reports": reports})

@role_required("student")
def report_form(request, pk=None):
    placement = _my_placement(request.user)
    if not placement:
        messages.error(request, "You have not been placed yet. Please wait for the admin.")
        return redirect("my_reports")
    if placement.status == Placement.COMPLETED:
        messages.error(request, "Your internship is completed; reports are closed.")
        return redirect("my_reports")
    inst = get_object_or_404(WeeklyReport, pk=pk, placement=placement) if pk else None
    form = ReportForm(request.POST or None, instance=inst, placement=placement)
    if request.method == "POST" and form.is_valid():
        r = form.save(commit=False)
        r.placement = placement
        r.status = WeeklyReport.SUBMITTED   # resubmitting sends it back for review
        r.reviewed_at = None
        r.save()
        messages.success(request, "Report submitted.")
        return redirect("my_reports")
    return render(request, "form.html", {"form": form, "title": "Weekly report", "cancel": reverse("my_reports")})

@role_required("supervisor")
def sup_reports(request):
    qs = WeeklyReport.objects.filter(placement__supervisor__user=request.user) \
        .select_related("placement__student__user", "placement__track")
    interns = Placement.objects.filter(supervisor__user=request.user).select_related("student__user", "track")
    return render(request, "reports/supervisor_reports.html", {
        "interns": interns,
        "pending": qs.filter(status=WeeklyReport.SUBMITTED),
        "reviewed": qs.filter(status=WeeklyReport.REVIEWED),
    })

@role_required("supervisor")
def review(request, pk):
    report = get_object_or_404(WeeklyReport, pk=pk, placement__supervisor__user=request.user)
    form = ReviewForm(request.POST or None, instance=report)
    if request.method == "POST" and form.is_valid():
        r = form.save(commit=False)
        r.status = WeeklyReport.REVIEWED
        r.reviewed_at = timezone.now()
        r.save()
        messages.success(request, "Feedback saved and report marked reviewed.")
        return redirect("sup_reports")
    return render(request, "reports/review.html", {"report": report, "form": form})


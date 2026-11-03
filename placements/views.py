from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from accounts.decorators import role_required
from .forms import StudentProfileForm, SupervisorForm, TrackForm, PlacementForm
from .models import StudentProfile, SupervisorProfile, Track, Placement

def _form_view(request, form_class, instance, title, back):
    form = form_class(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Saved.")
        return redirect(back)
    return render(request, "form.html", {"form": form, "title": title, "cancel": reverse(back)})

@role_required("student")
def profile(request):
    p, _ = StudentProfile.objects.get_or_create(user=request.user)
    return _form_view(request, StudentProfileForm, p, "My profile", "my_reports")

@role_required("admin")
def students(request):
    qs = StudentProfile.objects.select_related("user", "placement__track")
    return render(request, "placements/students.html", {"students": qs})

@role_required("admin")
def student_edit(request, pk):
    return _form_view(request, StudentProfileForm, get_object_or_404(StudentProfile, pk=pk), "Edit student", "students")

@role_required("admin")
def supervisors(request):
    return render(request, "placements/supervisors.html",
                  {"supervisors": SupervisorProfile.objects.select_related("user")})

@role_required("admin")
def supervisor_form(request, pk=None):
    inst = get_object_or_404(SupervisorProfile, pk=pk) if pk else None
    return _form_view(request, SupervisorForm, inst, "Supervisor", "supervisors")

@role_required("admin")
def tracks(request):
    return render(request, "placements/tracks.html", {"tracks": Track.objects.all()})

@role_required("admin")
def track_form(request, pk=None):
    inst = get_object_or_404(Track, pk=pk) if pk else None
    return _form_view(request, TrackForm, inst, "Track", "tracks")

@role_required("admin")
def placements(request):
    qs = Placement.objects.select_related("student__user", "supervisor__user", "track")
    return render(request, "placements/placements.html", {"placements": qs})

@role_required("admin")
def placement_form(request, pk=None):
    inst = get_object_or_404(Placement, pk=pk) if pk else None
    return _form_view(request, PlacementForm, inst, "Place a student", "placements")


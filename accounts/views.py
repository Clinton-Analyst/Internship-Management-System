from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import StudentRegisterForm, SupervisorRegisterForm
from .models import User

HOME = {User.STUDENT: "my_reports", User.SUPERVISOR: "sup_reports", User.ADMIN: "admin_dashboard"}

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "accounts/home.html", {
        "dashboard_url": HOME[request.user.role],
    })

def register(request):
    from placements.models import StudentProfile
    form = StudentRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = User.STUDENT
        user.save()
        StudentProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, "Account created. Complete your profile while an administrator arranges your placement.")
        return redirect("profile")
    return render(request, "form.html", {
        "form": form,
        "title": "Student registration",
        "submit_label": "Create account",
        "cancel": "/login/",
    })

def register_supervisor(request):
    from placements.models import SupervisorProfile

    form = SupervisorRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = User.SUPERVISOR
        user.save()
        SupervisorProfile.objects.create(
            user=user,
            organisation=form.cleaned_data["organisation"],
            phone=form.cleaned_data["phone"],
        )
        login(request, user)
        messages.success(request, "Account created. Please wait for an administrator to assign interns.")
        return redirect("sup_reports")
    return render(request, "form.html", {
        "form": form,
        "title": "Supervisor registration",
        "submit_label": "Create account",
        "cancel": "/login/",
    })

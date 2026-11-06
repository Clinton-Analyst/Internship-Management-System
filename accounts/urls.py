from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from . import views
from .forms import StyledPasswordResetForm, StyledSetPasswordForm

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        form_class=StyledPasswordResetForm,
        template_name="form.html",
        email_template_name="accounts/password_reset_email.txt",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done"),
        extra_context={
            "title": "Reset your password",
            "submit_label": "Send reset link",
            "cancel": "/login/",
        },
    ), name="password_reset"),
    path("password-reset/sent/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html",
    ), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        form_class=StyledSetPasswordForm,
        template_name="accounts/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete"),
    ), name="password_reset_confirm"),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html",
    ), name="password_reset_complete"),
    path("register/", views.register, name="register"),
    path("register/supervisor/", views.register_supervisor, name="register_supervisor"),
]


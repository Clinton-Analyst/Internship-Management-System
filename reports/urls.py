from django.urls import path
from . import views as v

urlpatterns = [
    path("reports/", v.my_reports, name="my_reports"),
    path("reports/new/", v.report_form, name="report_new"),
    path("reports/<int:pk>/edit/", v.report_form, name="report_edit"),
    path("supervisor/reports/", v.sup_reports, name="sup_reports"),
    path("supervisor/reports/<int:pk>/review/", v.review, name="report_review"),
]
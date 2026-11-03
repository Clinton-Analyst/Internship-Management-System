from django.urls import path
from . import views as v

urlpatterns = [
    path("profile/", v.profile, name="profile"),
    path("students/", v.students, name="students"),
    path("students/<int:pk>/edit/", v.student_edit, name="student_edit"),
    path("supervisors/", v.supervisors, name="supervisors"),
    path("supervisors/new/", v.supervisor_form, name="supervisor_new"),
    path("supervisors/<int:pk>/edit/", v.supervisor_form, name="supervisor_edit"),
    path("tracks/", v.tracks, name="tracks"),
    path("tracks/new/", v.track_form, name="track_new"),
    path("tracks/<int:pk>/edit/", v.track_form, name="track_edit"),
    path("placements/", v.placements, name="placements"),
    path("placements/new/", v.placement_form, name="placement_new"),
    path("placements/<int:pk>/edit/", v.placement_form, name="placement_edit"),
]

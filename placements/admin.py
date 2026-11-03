from django.contrib import admin
from .models import StudentProfile, SupervisorProfile, Track, Placement
for m in (StudentProfile, SupervisorProfile, Track, Placement):
    admin.site.register(m)


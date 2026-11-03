from django import forms
from accounts.forms import TailwindMixin
from accounts.models import User
from .models import StudentProfile, SupervisorProfile, Track, Placement

DATE = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})

class StudentProfileForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["reg_number", "programme", "department", "phone"]

    def clean_phone(self):
        p = self.cleaned_data["phone"].strip()
        if p and not p.replace("+", "").replace(" ", "").isdigit():
            raise forms.ValidationError("Phone may contain digits, spaces and a leading + only.")
        return p

class SupervisorForm(TailwindMixin, forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False,
                               help_text="Required for new supervisors; leave blank to keep the current one.")

    class Meta:
        model = SupervisorProfile
        fields = ["organisation", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            u = self.instance.user
            self.initial.update(username=u.username, first_name=u.first_name,
                                last_name=u.last_name, email=u.email)
            self.fields["username"].disabled = True

    def clean(self):
        c = super().clean()
        if not self.instance.pk:
            if not c.get("password"):
                self.add_error("password", "Password is required for a new supervisor.")
            if User.objects.filter(username=c.get("username")).exists():
                self.add_error("username", "That username is taken.")
        return c

    def save(self, commit=True):
        c = self.cleaned_data
        user = self.instance.user if self.instance.pk else User(username=c["username"], role=User.SUPERVISOR)
        user.first_name, user.last_name, user.email = c["first_name"], c["last_name"], c["email"]
        if c.get("password"):
            user.set_password(c["password"])
        user.save()
        profile = super().save(commit=False)
        profile.user = user
        profile.save()
        return profile

class TrackForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Track
        fields = ["name", "description", "is_active"]

class PlacementForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Placement
        fields = ["student", "supervisor", "track", "start_date", "end_date", "status"]
        widgets = {"start_date": DATE, "end_date": DATE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["track"].queryset = Track.objects.filter(is_active=True)

    def clean(self):
        c = super().clean()
        s, e = c.get("start_date"), c.get("end_date")
        if s and e and e <= s:
            self.add_error("end_date", "End date must be after the start date.")
        return c

from django import forms
from accounts.forms import TailwindMixin
from .models import WeeklyReport

class ReportForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ["week_number", "activities", "skills_learned", "challenges"]

    def __init__(self, *args, placement=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.placement = placement
        self.fields["week_number"].widget.attrs.update(min=1, max=placement.total_weeks() if placement else 52)

    def clean_week_number(self):
        w = self.cleaned_data["week_number"]
        if w < 1 or w > self.placement.total_weeks():
            raise forms.ValidationError(f"Week must be between 1 and {self.placement.total_weeks()}.")
        dup = WeeklyReport.objects.filter(placement=self.placement, week_number=w).exclude(pk=self.instance.pk)
        if dup.exists():
            raise forms.ValidationError("You already submitted this week. Edit it instead.")
        return w

class ReviewForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ["feedback"]

    def clean_feedback(self):
        f = self.cleaned_data["feedback"].strip()
        if len(f) < 5:
            raise forms.ValidationError("Please give meaningful feedback.")
        return f

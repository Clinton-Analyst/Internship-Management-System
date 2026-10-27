from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class TailwindMixin:
    """Gives every field the same kit (Tailwind classes)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            w = f.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs["class"] = "h-4 w-4"
            else:
                w.attrs["class"] = "w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600"
            if isinstance(w, forms.Textarea):
                w.attrs["rows"] = 4

class StudentRegisterForm(TailwindMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

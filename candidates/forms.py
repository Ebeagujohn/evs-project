from django import forms
from .models import Candidate


class CandidateForm(forms.ModelForm):
    """Form Admin uses to add a new candidate (FR1)."""

    class Meta:
        model = Candidate
        fields = ["name", "position"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Amaka Obi"}),
            "position": forms.TextInput(attrs={"placeholder": "e.g. Governor"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter the candidate's full name.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        position = cleaned_data.get("position")

        if name and position:
            # Duplicate check: same name + same position already exists
            if Candidate.objects.filter(name__iexact=name, position__iexact=position).exists():
                raise forms.ValidationError(
                    f'"{name}" is already registered for {position}.'
                )
        return cleaned_data
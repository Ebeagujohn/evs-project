from django import forms
from .models import Voter


class VoterRegistrationForm(forms.ModelForm):
    """Form voters fill in to register. Only these 3 fields are user-editable —
    voter_id, eligibility_status, and has_voted are set automatically by the
    model, not by the user."""

    class Meta:
        model = Voter
        fields = ["full_name", "age", "class_arm"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "e.g. Amina Yusuf"}),
            "age": forms.NumberInput(attrs={"placeholder": "e.g. 17"}),
            "class_arm": forms.TextInput(attrs={"placeholder": "e.g. SS3 Gold (optional)"}),
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is None:
            raise forms.ValidationError("Age is required.")
        if age < 1 or age > 100:
            raise forms.ValidationError("Enter a realistic age between 1 and 100.")
        return age

    def clean_full_name(self):
        name = self.cleaned_data.get("full_name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name
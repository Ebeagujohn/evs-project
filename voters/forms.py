from datetime import date
from django import forms
from .models import Voter, GENDER_CHOICES, NIGERIA_STATES


class VoterRegistrationForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=[("", "-- Select Gender --")] + GENDER_CHOICES
    )
    state_of_origin = forms.ChoiceField(
        choices=[("", "-- Select State --")] + NIGERIA_STATES
    )

    class Meta:
        model = Voter
        fields = ["full_name", "email", "date_of_birth", "gender", "state_of_origin", "photo"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "e.g. Amina Yusuf"}),
            "email": forms.EmailInput(attrs={"placeholder": "e.g. amina@example.com"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_full_name(self):
        name = self.cleaned_data.get("full_name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if Voter.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob is None:
            raise forms.ValidationError("Date of birth is required.")
        if dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")

        today = date.today()
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1

        if age < 18:
            raise forms.ValidationError(
                "You must be at least 18 years old to register. No Voter ID has been issued."
            )
        if age > 100:
            raise forms.ValidationError(
                "Registration is not available for this age. No Voter ID has been issued."
            )
        return dob
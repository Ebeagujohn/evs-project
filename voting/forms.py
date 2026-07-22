from django import forms
from voters.models import Voter
from candidates.models import Candidate
from .models import ElectionSettings

class VoterLoginForm(forms.Form):
    """Voter ID + email login (FR4). Requiring both makes blind guessing of
    sequential Voter IDs impractical without a full password system.
    Not a ModelForm — this doesn't create or edit a Voter record, it just
    looks one up and checks eligibility."""

    voter_id = forms.CharField(
        label="Voter ID",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "e.g. EVS-2026-0001"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "the email you registered with"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        voter_id = cleaned_data.get("voter_id", "").strip()
        email = cleaned_data.get("email", "").strip()

        if not voter_id or not email:
            return cleaned_data  # let the individual required-field errors show

        try:
            voter = Voter.objects.get(voter_id=voter_id, email__iexact=email)
        except Voter.DoesNotExist:
            # Deliberately generic — never reveal whether the ID or the
            # email was the wrong part, so a wrong guess can't be used
            # to enumerate valid Voter IDs one field at a time.
            raise forms.ValidationError("Voter ID or email not recognized.")

        if voter.eligibility_status != Voter.ELIGIBLE:
            raise forms.ValidationError("You are not eligible to vote yet.")

        if voter.has_voted:
            raise forms.ValidationError("You have already voted.")

        self.voter = voter
        return cleaned_data
    
    
class VoteForm(forms.Form):
    """The ballot itself — dynamically pulls every registered Candidate,
    never hard-coded (FR1/FR5)."""

    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
        error_messages={"required": "Please select a candidate before submitting."},
    )
class ElectionSettingsForm(forms.ModelForm):
    class Meta:
        model = ElectionSettings
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M"]# type: ignore
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M"]# type: ignore

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data
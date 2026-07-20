from django import forms
from voters.models import Voter
from candidates.models import Candidate
from .models import ElectionSettings

class VoterLoginForm(forms.Form):
    """Voter ID login (FR4). Not a ModelForm — this doesn't create or edit
    a Voter record, it just looks one up and checks three conditions."""

    voter_id = forms.CharField(
        label="Voter ID",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "e.g. EVS-2026-0001"}),
    )

    def clean_voter_id(self):
        voter_id = self.cleaned_data.get("voter_id", "").strip()

        try:
            voter = Voter.objects.get(voter_id=voter_id)
        except Voter.DoesNotExist:
            raise forms.ValidationError("Voter ID not found.")

        if voter.eligibility_status != Voter.ELIGIBLE:
            raise forms.ValidationError("You are not eligible to vote yet.")

        if voter.has_voted:
            raise forms.ValidationError("You have already voted.")

        self.voter = voter  # stash the found Voter object for the view to use
        return voter_id
    
    
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
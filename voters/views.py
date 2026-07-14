from django.shortcuts import render, redirect
from .forms import VoterRegistrationForm


def voters_register(request):
    """Handle voter self-registration (FR2, FR3)."""

    if request.method == "POST":
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            voter = form.save()  # triggers Voter.save() -> generates voter_id + eligibility
            return render(request, "voters/register_success.html", {"voter": voter})
        # if invalid, fall through and re-render the form WITH the errors
    else:
        form = VoterRegistrationForm()

    return render(request, "voters/register.html", {"form": form})
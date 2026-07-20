from django.shortcuts import render, redirect
from .forms import VoterRegistrationForm


def voters_register(request):
    """Handle voter self-registration (FR2, FR3)."""

    if request.method == "POST":
        # request.FILES carries the uploaded photo — request.POST alone
        # only carries text fields, so file uploads need both.
        # form = VoterRegistrationForm(request.POST, request.FILES)
        form = VoterRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            voter = form.save()
            return render(request, "voters/register_success.html", {"voter": voter})
    else:
        form = VoterRegistrationForm()

    return render(request, "voters/register.html", {"form": form})
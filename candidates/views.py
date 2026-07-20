from django.shortcuts import render
from evs_project.decorators import admin_required
from .forms import CandidateForm


@admin_required
def candidates_add(request):
    """Admin adds a new candidate (FR1). Requires staff login."""

    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            return render(request, "candidates/add_success.html", {"candidate": candidate})
    else:
        form = CandidateForm()

    return render(request, "candidates/add.html", {"form": form})


def candidates_access_denied(request):
    """Shown when a non-admin tries to reach an admin-only page.
    Shared by candidates, voting/results, and the dashboard."""
    return render(request, "candidates/access_denied.html")
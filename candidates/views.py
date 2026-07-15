from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CandidateForm


def admin_required(view_func):
    """Custom access control: if the user isn't logged in as staff, show a
    friendly error message and send them to our own access-denied page
    (which offers a proper login link) instead of Django's bare admin
    login screen."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You must be logged in as an admin to access that page.")
        return redirect("candidates:candidates_access_denied")

    return wrapper


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
    """Shown when a non-admin tries to reach the Add Candidate page."""
    return render(request, "candidates/access_denied.html")
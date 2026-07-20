"""
Shared access-control helper used by any app that has an admin-only page
(currently: candidates, voting/results, dashboard). Keeping it here means
all three pages behave identically instead of copy-pasting the same logic
three times.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """If the user isn't logged in as staff, show a friendly error message
    and send them to a proper access-denied page (with a working login
    link) instead of Django's bare admin login screen."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You must be logged in as an admin to access that page.")
        return redirect("candidates:candidates_access_denied")

    return wrapper
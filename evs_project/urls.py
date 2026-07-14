"""
URL configuration for evs_project project.

This is a SHARED file — all three apps are wired in here. Edit this together
as a team on a call; don't edit it solo, since it's the one file everyone's
work depends on.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Each app owns its own url namespace — see <app>/urls.py for routes.
    path('voters/', include('voters.urls')),
    path('candidates/', include('candidates.urls')),
    path('voting/', include('voting.urls')),
]
